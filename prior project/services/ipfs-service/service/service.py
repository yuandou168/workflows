import os
import time
import io
import threading
import ipfshttpclient
import psutil
from timeit import default_timer as timer
from multiprocessing.connection import Client, Listener
import threading
import requests

class Service():
    def __init__(self):
        if os.environ.get("BENCHMARK") is not None:
            self.bench_mark = True
        else:
            self.bench_mark = False

        if os.environ.get("OFFLINE_MODE") is not None:
            self.offline_mode = True
        else:
            self.offline_mode = False

        if os.environ.get("CHUNKER") is not None:
            self.chunker = os.environ["CHUNKER"]
        else:
            self.chunker = "size-262144"

        if os.environ.get("DAEMON_ADDRESS") is not None:
            self.daemon_address = os.environ["DAEMON_ADDRESS"]
        else:
            self.daemon_address = "/ip4/127.0.0.1/tcp/5001"

        if self.offline_mode is not None:
            self.bootstrap_address = os.environ["BOOTSTRAP_ADDRESS"]
        else:
            self.bootstrap_address = None            

        self.download_metrics = {}
        self.upload_metrics = {}

        is_connected = False

        while not is_connected:
            try:
                self.client = ipfshttpclient.connect(addr=self.daemon_address, session=True)

                self.peer_id = self.client.id()["ID"]
                self.root = "/ipns/" + self.peer_id
                
                is_connected = True
                print("Connected to IPFS daemon...")
            except Exception as exception:
                print(exception)
                time.sleep(1)

        if self.bootstrap_address is not None:
            # Start listening
            listen_thread = threading.Thread(target=self.listen_for_peers, args=[])
            listen_thread.start()
            
            # Connect to bootstrapping peer
            while True:
                try:
                    boostrap_peer = Client((self.bootstrap_address, 15000))

                    print("Connected to bootstrap peer...")

                    self.boostrap_peer_id = boostrap_peer.recv()

                    print("Received bootstrap peer id: " + self.boostrap_peer_id)

                    boostrap_peer.close()
                    break

                except Exception as exception:
                    print("Could not contact peer to acquire bootstrap peer ID")
                    print(exception)
                    time.sleep(1)

            if self.boostrap_peer_id != self.peer_id:
                while True:
                    bootstrap_address = "/ip4/" + self.bootstrap_address + "/tcp/4001/p2p/" + self.boostrap_peer_id

                    print(bootstrap_address)

                    try:
                        address_type = self.daemon_address.split("/")[1]
                        url = None
                        
                        if address_type == "dns":
                            url = "http://ipfs:5001/api/v0/swarm/connect"
                        else:
                            url = "http://127.0.0.1:5001/api/v0/swarm/connect"

                        response = requests.post(url, params={"arg": bootstrap_address})

                        break

                    except Exception as exception:
                        print("Could not bootstrap...")
                        print(exception)
                        time.sleep(1)
            else:
                print("I am the bootstrap peer")

        self.publish_periodically()

    def listen_for_peers(self):
        listener = None
        
        bind_attempts = 0
        while listener is None:
            try:
                listener = Listener(("0.0.0.0", 15000))
            except Exception as exception:
                print(exception)
                print("Could not bind to address")
                time.sleep(1)
                bind_attempts += 1
            
            if bind_attempts > 10:
                raise Exception("Failed to bind to address")

        while True:
            try:
                new_peer = listener.accept()

                print("New bootstrapping peer joined")

                new_peer.send(self.peer_id)

                print("Send my peer ID: " + self.peer_id)

                new_peer.close()
            except Exception as exception:
                print(exception)
                print("Could not accept bootstrapping peer...")
                time.sleep(1)

    def publish_periodically(self):
        """
        IPNS records have a 24 hour max lifetime. This function
        runs in the background and (re)publishes the records, ensuring
        that they can be accessed indefinitely.
        """
        try:
            self.publish_root()
        except Exception as exception:
            print("Could not publish files...")
            print(exception)

        # 6 hours
        threading.Timer(21600, self.publish_periodically).start()

    def get_peer_ids(self, path_hash):
        ids = set()

        # Skip the find provs command (throws exception: must be run in online mode)
        if self.offline_mode:
            ids.add(self.peer_id)
            return ids

        peers = self.client.dht.findprovs(cid=path_hash)

        # No one has this path hash
        if len(peers) == 0:
            return None

        for peer in peers:
            if peer["ID"] != "":
                ids.add(peer["ID"])
            elif peer["Responses"] != None and len(peer["Responses"]) != 0:
                for response in peer["Responses"]:
                    if response["ID"] != "":
                        ids.add(response["ID"])
        
        return ids

    def try_get_file_hash(self, peer_id, file_path):
        ipns_path = "/ipns/" + peer_id + file_path

        try:
            file_hash_bytes = self.client.cat(cid=ipns_path)
            file_hash_string = file_hash_bytes.decode("utf-8")
            return file_hash_string
        except Exception as exception:
            pass
        
        return None       

    def get_file_hash_from_peers(self, peer_ids, file_path):
        # If self peer_id is listed as in provs, return immediately
        if self.peer_id in peer_ids:
            file_hash = self.try_get_file_hash(self.peer_id, file_path)

            if file_hash != None:
                return file_hash
            else:
                peer_ids.remove(self.peer_id)

        # Else try getting it from others
        for peer_id in peer_ids:
            file_hash = self.try_get_file_hash(peer_id, file_path)

            if file_hash != None:
                return file_hash

        # Else no one has it, return None
        return None

    def get_file_path_hashed(self, file_path):
        file_path_bytes = io.BytesIO(bytes(file_path, "utf-8"))

        response = self.client.add(file=file_path_bytes, only_hash=True)

        return response["Hash"] 

    def download_file(self, file_hash, file_path):
        split = file_path.split("/")
        file_name = split[len(split) - 1]

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        self.client.get(cid=file_hash + "/" + file_name, target=os.path.dirname(file_path))
    
    def download(self, file_path):
        """
        Given an file path, this function will attempt to find who has it and 
        then proceed to download it.
        """
        try:
            if self.bench_mark:
                self.download_metrics["1"] = self.log_metrics()
            
            # Get the file path but hashed through IPFS
            path_hash = self.get_file_path_hashed(file_path=file_path)

            if self.bench_mark:
                self.download_metrics["2"] = self.log_metrics()

            # Find peers that added the file hash (should only be 1 peer
            # unless other peers uploaded a file to the same local file path)
            peer_ids = self.get_peer_ids(path_hash=path_hash)

            if peer_ids is None:
                return (False, "No peers were found with the path hash")

            if self.bench_mark:
                self.download_metrics["3"] = self.log_metrics()

            # Get a reference to the file hash needed to download the file
            file_hash = self.get_file_hash_from_peers(peer_ids=peer_ids, file_path=file_path)

            if file_hash is None:
                return (False, "Could not obtain file hash from peers")

            if self.bench_mark:
                self.download_metrics["4"] = self.log_metrics()

            # Download the actual file into the same local file path from where it was uploaded
            self.download_file(file_hash=file_hash, file_path=file_path)

            if self.bench_mark:
                self.download_metrics["5"] = self.log_metrics()

            # OPTIONAL: Pin/advertise the file so that other peers can fetch the reference from here
            # # Write file hash to MFS, so other peers can fetch it from here
            # self.write_file_hash_to_mfs(file_hash=file_hash, file_path=file_path)
            
            # if self.bench_mark:
            #     self.download_metrics["6"] = self.log_metrics()

            # # Add the hashed path, advertising that it also now has the reference to the file hash
            # self.client.add_str(string=file_path)

            # if self.bench_mark:
            #     self.download_metrics["7"] = self.log_metrics()

            # # Pin the file itself, so that it doesn't get garbage collected
            # # Peers already advertise themselves as having it (until it is garbage collected)
            # self.client.pin.add(path=file_hash)

            # if self.bench_mark:
            #     self.download_metrics["8"] = self.log_metrics()

            return (True, None)

        except Exception as exception:
            # print("DOWNLOAD EXCEPTION: " + str(exception))
            return (False, str(exception))

    def add_file_wrapped(self, file_path):
        file_hashes = self.client.add(file=file_path, wrap_with_directory=True, chunker=self.chunker)
        
        for file_hash in file_hashes:
            if file_hash["Name"] == "":
                return file_hash["Hash"]
        
        return None

    def get_local_file_hash(self, file_path):
        try:
            file_hash_bytes = self.client.files.read(file_path)

            file_hash_string = file_hash_bytes.decode("utf-8")

            return file_hash_string
        except:
            return None

    def write_file_hash_to_mfs(self, file_hash, file_path):
        existing_file_hash = self.get_local_file_hash(file_path)

        # A file hash was already written there
        if existing_file_hash != None:
            # Check if it is different
            if existing_file_hash != file_hash:
                # If so, unpin is and let it be garbage collected later
                self.client.pin.rm(path=existing_file_hash)

        self.client.files.mkdir(path=os.path.dirname(file_path), parents=True)

        file_hash_bytes = io.BytesIO(bytes(file_hash, encoding="utf-8"))
        
        self.client.files.write(path=file_path, file=file_hash_bytes, create=True)  

    def upload(self, file_path):
        """
        Given a file path, this function writes it to the MFS and publishes the root
        """
        try:
            if self.bench_mark:
                self.upload_metrics["1"] = self.log_metrics()

            # Add the file wrapped within the directory (due to a bug in ipfshttpclient outputting the hash during download as filename)
            file_hash = self.add_file_wrapped(file_path)

            if file_hash is None:
                return (False, "Could not upload the file")

            if self.bench_mark:
                self.upload_metrics["2"] = self.log_metrics()

            # Write the hash to MFS
            self.write_file_hash_to_mfs(file_hash=file_hash, file_path=file_path)

            if self.bench_mark:
                self.upload_metrics["3"] = self.log_metrics()

            # Publish the root of MFS
            self.publish_root()

            if self.bench_mark:
                self.upload_metrics["5"] = self.log_metrics()

            # Add the hashed local path to advertise that this peer has the file
            self.client.add_str(file_path)

            if self.bench_mark:
                self.upload_metrics["6"] = self.log_metrics()

            return (True, None)

        except Exception as exception:
            print("UPLOAD EXCEPTION: " + str(exception))
            return (False, str(exception))

    def publish_root(self):
        """
        Published the root of the MFS.
        """
        # Get the hash of the root
        root_hash = self.client.files.stat(path="/")["Hash"]

        if self.bench_mark:
            self.upload_metrics["4"] = self.log_metrics()

        # Publish this root hash (1ns ttl forces peers to fetch it from DHT, instead of retrieving it from stale cache)
        self.client.name.publish(ipfs_path=root_hash, allow_offline=True, lifetime="24h", resolve=True, ttl="1ns")

    def delete(self, file_path):
        """
        Deletes the file from the MFS.
        """
        try:
            # Unpin the file referencing the file
            path_hash = self.get_file_path_hashed(file_path=file_path)
            self.client.pin.rm(path=path_hash)
         
            # Unpin the file itself
            file_hash = self.get_local_file_hash(file_path)
            self.client.pin.rm(path=file_hash)

            # Delete the hash from MFS
            self.client.files.rm(path=file_path, recursive=False)

            # Republish root
            self.publish_root()

            # Run garbage collector
            self.client.repo.gc(quiet=True)

            return (True, None)

        except Exception as exception:
            print("DELETE EXCEPTION: " + str(exception))
            return (False, str(exception))

    def metrics(self):
        return {"download": self.download_metrics, "upload": self.upload_metrics}

    def log_metrics(self):
        row = list(range(18))
        
        row[0] = timer()
        row[1] = time.time()

        cpu = psutil.cpu_times(percpu=False)
        row[2] = cpu.user
        row[3] = cpu.system
        row[4] = cpu.idle
        if hasattr(cpu, "iowait"):
            row[5] = cpu.iowait

        disk = psutil.disk_io_counters(perdisk=False)
        row[6] = disk.read_bytes
        row[7] = disk.write_bytes
        row[8] = disk.read_count
        row[9] = disk.write_count

        mem = psutil.virtual_memory()
        row[10] = mem.available
        row[11] = mem.used
        row[12] = mem.free
        if hasattr(mem, "cached"):
            row[13] = mem.cached

        net = psutil.net_io_counters(pernic=True)
        if "lo" in net:
            lo = net["lo"]
            row[14] = lo.bytes_sent
            row[15] = lo.bytes_recv
        if "eth0" in net:
            eth_0 = net["eth0"]
            row[16] = eth_0.bytes_sent
            row[17] = eth_0.bytes_recv
        
        return row 