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
file_in = args["file_in"]
interface = Client()
success = False
attempts = 1
while not success:
    success = interface.download(file_in)
    if not success:
        attempts += 1
    if attempts > 10000:
        raise Exception("Failed to download file {}".format(file_in))
time_download = time.time()
print("({}) Downloaded file {} of size {} bytes in {} attempt(s)".format(
    time.strftime("%H:%M:%S", time.localtime(time_download)), 
    file_in, 
    os.path.getsize(file_in), 
    attempts
))

# Partition
file_object = open(file_in, "rb", 0)
byte_array = file_object.read()
file_object.close()
files_out = args["files_out"]
byte_array_length = len(byte_array)
chunk_size = int(byte_array_length / len(files_out))
current_chunk = 0
for file_out in files_out:
    slice_start = current_chunk * chunk_size
    slice_end = slice_start + chunk_size
    byte_array_slice = byte_array[slice_start:slice_end]

    file_object = open(file_out, "wb", 0)
    file_object.write(byte_array_slice)
    file_object.close()

    current_chunk += 1
time_partition = time.time()
print("({}) Partitioned file {} into files {} of size {} bytes".format(
    time.strftime("%H:%M:%S", time.localtime(time_partition)), 
    file_in,
    files_out, 
    chunk_size
))

# Upload files
interface = Client()
for file_out in files_out:
    success = interface.upload(file_out)
    if not success:
        raise Exception("Failed to upload file {}".format(file_out))
time_upload = time.time()
print("({}) Uploaded files {} of size {}".format(
    time.strftime("%H:%M:%S", time.localtime(time_upload)), 
    files_out, 
    byte_array_length
))

# Delete local files
os.remove(file_in)
for file_out in files_out:
    os.remove(file_out)

# Write log to disk
task_log = "/tmp/logs/{}/{}".format(run_id, task_id)
with open(task_log, "w") as file_object:
    file_object.write(json.dumps({
        "time_start": time_start,
        "time_download": time_download,
        "time_partition": time_partition,
        "time_upload": time_upload
    }))
    file_object.truncate()

