from benchmark_runner import docker_pull, docker_compose_run
from benchmark_parameters import file_sizes, run_count, interval_seconds
from multiprocessing.connection  import Client
import time

docker_pull(container="nicoja/client-container", output_file="/tmp/client-container.log")

time.sleep(10)

server_address = "172.21.0.4"
server =  Client((server_address, 12000))

for file_size_name, file_size in file_sizes.items():
    # Continue benchmark?
    server.send(True)

    # Wait for FTP server finished startup signal
    server.recv()

    environment = {
        "SCRIPT": "transfer_ftp_upload.py",
        "FTP_SERVER_ADDRESS": server_address,
        "FILE_SIZE": str(file_size),
        "RUN_COUNT": str(run_count),
        "INTERVAL_SECONDS": str(interval_seconds),
    }

    docker_compose_run (
        compose_file="/tmp/transfer_ftp_client_setup.yml",
        output_file="/tmp/logs/transfer_ftp_upload_" + file_size_name + ".log",
        environment=environment,
    )

    environment = {
        "SCRIPT": "transfer_ftp_download.py",
        "FTP_SERVER_ADDRESS": server_address,
        "FILE_SIZE": str(file_size),
        "RUN_COUNT": str(run_count),
        "INTERVAL_SECONDS": str(interval_seconds),
    }

    docker_compose_run (
        compose_file="/tmp/transfer_ftp_client_setup.yml",
        output_file="/tmp/logs/transfer_ftp_download_" + file_size_name + ".log",
        environment=environment,
    )

    # Send teardown
    server.send(True)
    
    # Receive teardown complete
    server.recv()

server.send(False)
server.close()