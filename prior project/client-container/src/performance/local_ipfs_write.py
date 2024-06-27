import os
import gc
import time

from util_metrics import log_metrics, log_event
from util_files import create_bytes, create_file, delete_file, write_json
from util_env import file_size, file_size_name, run_count, interval_seconds

from client import Client

log_event("Waiting for 20 seconds for setup to finish")
time.sleep(20)

log_event("Starting " + file_size_name + " benchmark")

log_event("Creating client interface")
interface = Client(os.environ["SERVICE_ADDRESS"])

runs = []

for count in range(run_count):
    run_id = str(count + 1)
    log_event("Preparing run " + run_id)

    log_event("Creating random byte array of " + file_size_name)
    file_bytes = create_bytes(file_size)

    file_path = "/tmp/files/" + file_size_name + "_" + run_id
    log_event("Output location is " + file_path)

    log_event("Running garbage collector")
    gc.collect()

    log_event("Sleeping for " + str(interval_seconds) + " seconds")
    time.sleep(interval_seconds)

    log_event("Starting")
    run = {}
    run["1"] = log_metrics()

    file_object = open(file_path, "wb", 0)
    file_object.write(file_bytes)
    file_object.close()

    run["2"] = log_metrics()

    success = interface.upload(file_path)
    if success == False:
        raise Exception("Failed to upload the file")

    run["9"] = log_metrics()
    log_event("Finished")

    log_event("Collecting metrics from service")
    service_metrics = interface.metrics()
    run["3"] = service_metrics["upload"]["1"]
    run["4"] = service_metrics["upload"]["2"]
    run["5"] = service_metrics["upload"]["3"]
    run["6"] = service_metrics["upload"]["4"]
    run["7"] = service_metrics["upload"]["5"]
    run["8"] = service_metrics["upload"]["6"]
    runs.append(run)

    log_event("Deleting created file " + file_path)
    delete_file(file_path)

    log_event("Deleting uploaded file " + file_path)
    interface.delete(file_path)

    log_event("Ending run " + run_id)

log_event("Writing metrics file")
write_json(file_name="local_ipfs_write_" + file_size_name, json_data=runs)

