from benchmark_runner import docker_pull, docker_compose_run
from benchmark_parameters import file_sizes, run_count, interval_seconds
from multiprocessing.connection  import Client
import time

docker_pull(container="nicoja/client-container", output_file="/tmp/client-container.log")
docker_pull(container="nicoja/webdav-service2", output_file="/tmp/webdav-service.log")

time.sleep(10)

server_ip = "172.21.0.4"
server_address = "http://" + server_ip + ":80"
server_connection = Client((server_ip, 12000))

for file_size_name, file_size in file_sizes.items():
    # Continue benchmark?
    server_connection.send(True)

    # Wait for WebDAV server finished startup signal
    server_connection.recv()

    environment = {
        "SCRIPT": "transfer_webdav_upload.py",
        "HOST_ADDRESS": server_address,
        "FILE_SIZE": str(file_size),
        "RUN_COUNT": str(run_count),
        "INTERVAL_SECONDS": str(interval_seconds),
    }

    docker_compose_run (
        compose_file="/tmp/transfer_webdav_client_setup.yml",
        output_file="/tmp/logs/transfer_webdav_upload_" + file_size_name + ".log",
        environment=environment,
    )

    environment = {
        "SCRIPT": "transfer_webdav_download.py",
        "HOST_ADDRESS": server_address,
        "FILE_SIZE": str(file_size),
        "RUN_COUNT": str(run_count),
        "INTERVAL_SECONDS": str(interval_seconds),
    }

    docker_compose_run (
        compose_file="/tmp/transfer_webdav_client_setup.yml",
        output_file="/tmp/logs/transfer_webdav_download_" + file_size_name + ".log",
        environment=environment,
    )

    # Send teardown
    server_connection.send(True)
    
    # Receive teardown complete
    server_connection.recv()

server_connection.send(False)
server_connection.close()