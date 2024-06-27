import os
import gc
import time

from util_metrics import log_metrics, log_event
from util_files import create_bytes, create_file, delete_file, write_json
from util_env import file_size, file_size_name, run_count, interval_seconds

from multiprocessing.connection import Client as ClientConnection

from client import Client

time.sleep(5)

log_event("Connecting to download script runner")
download_peer = ClientConnection(("127.0.0.1", 12001))

log_event("Waiting for finish upload signal")
# Start download signal
download_peer.recv()

log_event("Starting " + file_size_name + " benchmark")
log_event("Creating client interface")
interface = Client(os.environ["SERVICE_ADDRESS"])

runs = []

for count in range(run_count):
    run_id = str(count + 1)
    log_event("Preparing run " + run_id)

    file_path = "/tmp/files/" + file_size_name + "_" + run_id
    log_event("Download file name is " + file_path)

    log_event("Running garbage collector")
    gc.collect()

    log_event("Sleeping for " + str(interval_seconds) + " seconds")
    time.sleep(interval_seconds)
    
    log_event("Starting")
    run = {}
    run["1"] = log_metrics()

    success = interface.download(file_path)
    if success == False:
        raise Exception("Failed to download the file")

    run["7"] = log_metrics()
    log_event("Finished")

    log_event("Collecting metrics from service")
    service_metrics = interface.metrics()
    run["2"] = service_metrics["download"]["1"]
    run["3"] = service_metrics["download"]["2"]
    run["4"] = service_metrics["download"]["3"]
    run["5"] = service_metrics["download"]["4"]
    run["6"] = service_metrics["download"]["5"]
    runs.append(run)

    log_event("Deleting downloaded file " + file_path)
    delete_file(file_path)

    log_event("Ending run " + run_id)

log_event("Writing metrics file")
write_json(file_name="transfer_ipfs_download_" + file_size_name, json_data=runs)

log_event("Send finished download signal")
# Send finished downloading signal
download_peer.send(True)