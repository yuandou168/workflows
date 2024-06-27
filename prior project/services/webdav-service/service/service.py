from webdav3.client import Client
from requests.auth import HTTPDigestAuth
from pathlib import Path
from timeit import default_timer as timer
import psutil
import time
import os

class Service():
    def __init__(self):
        if os.environ.get("BENCHMARK") is not None:
            self.bench_mark = True
        else:
            self.bench_mark = False
            
        self.download_metrics = {}
        self.upload_metrics = {}

        host_address = os.environ["HOST_ADDRESS"]
        login = os.environ["USERNAME"]
        password = os.environ["PASSWORD"]
        
        is_connected = False

        while not is_connected:
            try:
                self.client = Client({"webdav_hostname": host_address})
                self.client.session.auth = HTTPDigestAuth(login, password)
                self.client.info("/")

                is_connected = True
                print("Connected to WebDAV server...")
            except Exception as exception:
                print(exception)
                time.sleep(1)
        
    def download(self, file_path):
        """
        Given an absolute filepath as <file_path>, this function will download
        it to the same location on the host.
        """
        try:
            if self.bench_mark:
                self.download_metrics["1"] = self.log_metrics()

            # Ensure output directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Download the file synchronously
            self.client.download_sync(remote_path=file_path, local_path=file_path)

            if self.bench_mark:
                self.download_metrics["2"] = self.log_metrics()

            return (True, None)

        except Exception as exception:
            print(exception)
            return (False, str(exception))
        
    def upload(self, file_path):
        """
        Given an absolute file path as <file_path>, this function will upload
        the file to the same location on WebDAV and return the file path (which
        is the same as the local file path).
        """
        try:
            if self.bench_mark:
                self.upload_metrics["1"] = self.log_metrics()

            # Create remote directories on WebDAV, mirroring the local path
            structure = Path(file_path).parent
            combined = ""
            for part in structure.parts:
                combined += str(part)
                
                if str(part) != "/":
                    combined += "/"

                self.client.mkdir(combined)

            if self.bench_mark:
                self.upload_metrics["2"] = self.log_metrics()

            # Upload the file
            self.client.upload_sync(remote_path=file_path, local_path=file_path)

            if self.bench_mark:
                self.upload_metrics["3"] = self.log_metrics()

            return (True, None)

        except Exception as exception:
            print(exception)
            return (False, str(exception))

    def delete(self, file_path):
        """
        Delete the file given the file path.
        """
        try:
            self.client.clean(file_path)

            return (True, None)

        except Exception as exception:
            print(exception)
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