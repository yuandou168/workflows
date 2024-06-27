import os
import time
import json
import sys
import socket
from client import Client

# Start
args = json.loads(sys.argv[1])
task_id = args["task_id"]
run_id = args["run_id"]
scenario = args["scenario"]
data_mesh = args["data_mesh"]
file_size = args["file_size"]
location = socket.gethostname()
time_start = time.time()
print("({}) Started task {}-{} with {}_{}_{} at {}".format(
    time.strftime("%H:%M:%S", time.localtime(time_start)),
    run_id,
    task_id,
    scenario,
    data_mesh,
    file_size,
    location
))

# Download
files_in = args["files_in"]
interface = Client()
combined_attempts = 0
combined_size = 0
for file_in in files_in:
    success = False
    attempts = 1
    while not success:
        success = interface.download(file_in)
        if not success:
            attempts += 1
        if attempts > 10000:
            raise Exception("Failed to download file {}".format(file_in))

    combined_size += os.path.getsize(file_in)
    combined_attempts += attempts
time_download = time.time()
print("({}) Downloaded files {} of combined size {} bytes in combined {} attempt(s)".format(
    time.strftime("%H:%M:%S", time.localtime(time_download)), 
    files_in, 
    combined_size, 
    combined_attempts
))

# Merge
file_out = args["file_out"]
file_out_object = open(file_out, "wb", 0)
for file_in in files_in:
    file_in_object = open(file_in, "rb", 0)
    contents = file_in_object.read()
    file_in_object.close()
    file_out_object.write(contents)
file_out_object.close()
file_out_size = os.path.getsize(file_out)
time_merge = time.time()
print("({}) Merged files {} into single file {} of size {} bytes".format(
    time.strftime("%H:%M:%S", time.localtime(time_merge)), 
    files_in, 
    file_out,
    file_out_size
))

# Upload
interface = Client()
success = interface.upload(file_out)
if not success:
    raise Exception("Failed to upload file {}".format(file_out))
time_upload = time.time()
print("({}) Uploaded file {} of size {}".format(
    time.strftime("%H:%M:%S", time.localtime(time_upload)), 
    file_out, 
    file_out_size
))

# Delete local files
for file_in in files_in:
    os.remove(file_in)
os.remove(file_out)

# Write log to disk
task_log = "/tmp/logs/{}/{}".format(run_id, task_id)
with open(task_log, "w") as file_object:
    file_object.write(json.dumps({
        "time_start": time_start,
        "time_download": time_download,
        "time_merge": time_merge,
        "time_upload": time_upload
    }))
    file_object.truncate()