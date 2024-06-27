import os
import gc
import time

from util_metrics import log_metrics, log_event
from util_files import create_bytes, create_file, delete_file, write_json
from util_env import file_size, file_size_name, run_count, interval_seconds

log_event("Starting " + file_size_name + " benchmark")

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
    runs.append(run)
    log_event("Finished")

    log_event("Deleting created file " + file_path)
    delete_file(file_path)

    log_event("Ending run " + run_id)

log_event("Writing metrics file")
write_json(file_name="local_disk_write_" + file_size_name, json_data=runs)