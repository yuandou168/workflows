from benchmark_runner import docker_pull, docker_compose_run_daemon, docker_compose_kill_daemon

import sys
import time
from multiprocessing.connection  import Listener

docker_pull (container="bytemark/webdav:2.4", output_file="/tmp/webdav.log")

listener = Listener(("0.0.0.0", 12000))
client_connection = listener.accept()

while client_connection.recv():
    webdav_server = docker_compose_run_daemon(compose_file="/tmp/transfer_webdav_server_setup.yml")
    time.sleep(5)

    # WebDAV server ready
    client_connection.send(True)

    # Receive teardown signal
    client_connection.recv()

    docker_compose_kill_daemon(compose_file="/tmp/transfer_webdav_server_setup.yml", daemon=webdav_server)

    # Finished teardown
    client_connection.send(True)

client_connection.close()