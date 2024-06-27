import os
import gc
import time

from util_metrics import log_metrics, log_event
from util_files import create_bytes, create_file, delete_file, write_json
from util_env import file_size, file_size_name, run_count, interval_seconds

from client import Client

time.sleep(10)

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
    if not success:
        raise Exception("Failed to upload the file")

    run["5"] = log_metrics()
    log_event("Finished")

    log_event("Collecting metrics from service")
    service_metrics = interface.metrics()
    run["2"] = service_metrics["upload"]["1"]
    run["3"] = service_metrics["upload"]["2"]
    run["4"] = service_metrics["upload"]["3"]
    runs.append(run)

    log_event("Deleting created file " + file_path)
    delete_file(file_path)

    log_event("Ending run " + run_id)

write_json(file_name="transfer_webdav_upload_" + file_size_name, json_data=runs)