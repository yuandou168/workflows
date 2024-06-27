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

# Create
file_size = args["file_size"]
file_out = args["file_out"]
byte_array = os.urandom(file_size)
file_object = open(file_out, "wb", 0)
file_object.write(byte_array)
file_object.close()
time_create = time.time()
print("({}) Created file {} of size {} bytes".format(
    time.strftime("%H:%M:%S", time.localtime(time_create)), 
    file_out, 
    file_size
))

# Upload
interface = Client()
success = interface.upload(file_out)
if not success:
    raise Exception("Failed to upload file {}".format(file_out))
time_upload = time.time()
print("({}) Uploaded file {} of size {} bytes".format(
    time.strftime("%H:%M:%S", time.localtime(time_upload)), 
    file_out, 
    file_size
))

# Delete local file
os.remove(file_out)

# Write log to disk
task_log = "/tmp/logs/{}/{}".format(run_id, task_id)
with open(task_log, "w") as file_object:
    file_object.write(json.dumps({
        "time_start": time_start,
        "time_create": time_create,
        "time_upload": time_upload
    }))
    file_object.truncate()