from benchmark_runner import docker_pull, docker_compose_run
from benchmark_parameters import file_sizes, run_count, interval_seconds
from multiprocessing.connection import Listener

docker_pull(container="nicoja/ipfs-node", output_file="/tmp/ipfs-node.log")
docker_pull(container="nicoja/ipfs-service2", output_file="/tmp/ipfs-service2.log")
docker_pull(container="nicoja/client-container", output_file="/tmp/client-container.log")

download_peer_listener = Listener(("0.0.0.0", 12000))
download_peer = download_peer_listener.accept()

def synchronizer(download_peer):
    upload_container_listener = Listener(("127.0.0.1", 12001))
    upload_container = upload_container_listener.accept()

    # Send peer ID to download container for it to bootstrap
    peer_id = upload_container.recv()
    download_peer.send(peer_id)

    # Wait for download peer to start
    download_peer.recv()

    # Start uploading
    upload_container.send(True)

    # Wait for it to finish uploading
    upload_container.recv()

    # Download peer may start downloading
    download_peer.send(True)

    # Wait for downloading to finish
    download_peer.recv()

    # Finish process
    upload_container.send(True)

for file_size_name, file_size in file_sizes.items():
    environment = {
        "SCRIPT": "transfer_ipfs_upload.py",
        "FILE_SIZE": str(file_size),
        "RUN_COUNT": str(run_count),
        "INTERVAL_SECONDS": str(interval_seconds),
    }

    docker_compose_run (
        compose_file="/tmp/transfer_ipfs_upload_setup.yml",
        output_file="/tmp/logs/transfer_ipfs_upload_" + file_size_name + ".log",
        environment=environment,
        call_back=lambda: synchronizer(download_peer),
    )