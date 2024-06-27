import time
from benchmark_runner import docker_pull, docker_compose_run
from benchmark_parameters import file_sizes, run_count, interval_seconds
from multiprocessing.connection import Client, Listener

docker_pull(container="nicoja/ipfs-node", output_file="/tmp/ipfs-node.log")
docker_pull(container="nicoja/ipfs-service2", output_file="/tmp/ipfs-service2.log")
docker_pull(container="nicoja/client-container", output_file="/tmp/client-container.log")

time.sleep(10)

# VM1
upload_peer_address = "172.21.0.4"
upload_peer = Client((upload_peer_address, 12000))

def synchronizer(upload_peer):
    download_container_listener = Listener(("127.0.0.1", 12001))
    download_container = download_container_listener.accept()
    
    # Download peer is connected
    upload_peer.send(True)

    # Get download start signal
    upload_peer.recv()

    # Start downloading
    download_container.send(True)

    # Wait for downloading to finish
    download_container.recv()

    # Send downloading finished signal
    upload_peer.send(True)


for file_size_name, file_size in file_sizes.items():
    peer_id = upload_peer.recv()

    environment = {
        "SCRIPT": "transfer_ipfs_download.py",
        "PEER_ID": peer_id,
        "BOOT_ADDRESS":  upload_peer_address,
        "FILE_SIZE": str(file_size),
        "RUN_COUNT": str(run_count),
        "INTERVAL_SECONDS": str(interval_seconds),
    }

    docker_compose_run (
        compose_file="/tmp/transfer_ipfs_download_setup.yml",
        output_file="/tmp/logs/transfer_ipfs_download_" + file_size_name + ".log",
        environment=environment,
        call_back=lambda: synchronizer(upload_peer),
    )