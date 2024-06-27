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

# Read
file_object = open(file_in, "rb", 0)
byte_array = file_object.read()
file_object.close()
time_read = time.time()
print("({}) Read file {} with length of {} bytes".format(
    time.strftime("%H:%M:%S", time.localtime(time_read)), 
    file_in, 
    len(byte_array)
))

# Delete local file
os.remove(file_in)

# Write log to disk
task_log = "/tmp/logs/{}/{}".format(run_id, task_id)
with open(task_log, "w") as file_object:
    file_object.write(json.dumps({
        "time_start": time_start,
        "time_download": time_download,
        "time_read": time_read
    }))
    file_object.truncate()