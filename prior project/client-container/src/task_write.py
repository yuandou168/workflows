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


# Time download
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

# Time read
file_object = open(file_in, "rb", 0)
byte_array = file_object.read()
byte_array_length = len(byte_array)
file_object.close()
del byte_array
time_read = time.time()
print("({}) Read file {} of size {} bytes".format(
    time.strftime("%H:%M:%S", time.localtime(time_read)), 
    file_in, 
    byte_array_length
))

# Time write
file_out = args["file_out"]
byte_array = os.urandom(byte_array_length)
file_object = open(file_out, "wb", 0)
file_object.write(byte_array)
file_object.close()
time_write = time.time()
print("({}) Wrote file {} of size {} bytes".format(
    time.strftime("%H:%M:%S", time.localtime(time_write)), 
    file_out, 
    byte_array_length
))

# Time upload
interface = Client()
success = interface.upload(file_out)
if not success:
    raise Exception("Failed to upload file {}".format(file_out))
time_upload = time.time()
print("({}) Uploaded file {} of size {}".format(
    time.strftime("%H:%M:%S", time.localtime(time_upload)), 
    file_out, 
    byte_array_length
))

# Delete local files
os.remove(file_in)
os.remove(file_out)

# Write log to disk
task_log = "/tmp/logs/{}/{}".format(run_id, task_id)
with open(task_log, "w") as file_object:
    file_object.write(json.dumps({
        "time_start": time_start,
        "time_download": time_download,
        "time_read": time_read,
        "time_write": time_write,
        "time_upload": time_upload
    }))
    file_object.truncate()