import os
import gc
import time

from util_metrics import log_metrics, log_event
from util_files import create_bytes, create_file, delete_file, write_json
from util_env import file_size, file_size_name, run_count, interval_seconds

from multiprocessing.connection import Client as ClientConnection

from client import Client

import ipfshttpclient

time.sleep(5)

log_event("Connecting to IPFS daemon")
ipfs_client = None
ipfs_daemon_running = False
while not ipfs_daemon_running:
    try:
        ipfs_client = ipfshttpclient.connect(addr="/ip4/127.0.0.1/tcp/5001")
        ipfs_daemon_running = True
    except Exception as exception:
        print(exception)
        time.sleep(1)
peer_id = ipfs_client.id()["ID"]
log_event("Connected to IPFS daemon, peer ID is " + peer_id)

log_event("Connecting to upload script runner")
upload_peer = ClientConnection(("127.0.0.1", 12001))

log_event("Sending peer ID")
upload_peer.send(peer_id)

log_event("Waiting for signal to start downloading")
upload_peer.recv()

log_event("Starting " + file_size_name + " benchmark")
log_event("Creating client interface")
interface = Client(os.environ["SERVICE_ADDRESS"])

runs = []
for count in range(run_count):
    run_id = str(count + 1)
    log_event("Preparing run " + run_id)

    file_path = "/tmp/files/" + file_size_name + "_" + run_id
    log_event("Creating file " + file_path)
    create_file(file_size, file_path)

    log_event("Running garbage collector")
    gc.collect()

    log_event("Sleeping for " + str(interval_seconds) + " seconds")
    time.sleep(interval_seconds)

    log_event("Starting")
    run = {}
    run["1"] = log_metrics()

    success = interface.upload(file_path)
    if success == False:
        raise Exception("Failed to upload the file")

    run["8"] = log_metrics()
    log_event("Finished")

    log_event("Collecting metrics from service")
    service_metrics = interface.metrics()
    run["2"] = service_metrics["upload"]["1"]
    run["3"] = service_metrics["upload"]["2"]
    run["4"] = service_metrics["upload"]["3"]
    run["5"] = service_metrics["upload"]["4"]
    run["6"] = service_metrics["upload"]["5"]
    run["7"] = service_metrics["upload"]["6"]
    runs.append(run)

    log_event("Deleting created file " + file_path)
    delete_file(file_path)

    log_event("Ending run " + run_id)

log_event("Writing metrics file")
write_json(file_name="transfer_ipfs_upload_" + file_size_name, json_data=runs)

log_event("Sending upload finished signal")
# Finished upload signal
upload_peer.send(True)

log_event("Waiting for download finished signal")
# Finished download signal
upload_peer.recv()