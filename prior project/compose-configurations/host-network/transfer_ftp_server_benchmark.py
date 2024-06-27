from benchmark_runner import docker_pull, docker_compose_run_daemon, docker_compose_kill_daemon

import sys
import time
from multiprocessing.connection  import Listener

docker_pull (
  container="stilliard/pure-ftpd@sha256:1d15f8091b18d399178acc47559b9328c3deecca732d52df96e65303d6a8a966", 
  output_file="/tmp/pure-ftpd.log"
)

listener = Listener(("0.0.0.0", 12000))
client = listener.accept()

while client.recv():
    ftp_server = docker_compose_run_daemon(compose_file="/tmp/transfer_ftp_server_setup.yml")
    time.sleep(5)

    # FTP server ready
    client.send(True)

    # Receive teardown signal
    client.recv()

    docker_compose_kill_daemon(compose_file="/tmp/transfer_ftp_server_setup.yml", daemon=ftp_server)

    # Finished teardown
    client.send(True)

client.close()