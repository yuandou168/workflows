import os
import sys
import json
import time
import socket
import psutil
from client import Client

args = json.loads(sys.argv[1])
run_id = args["run_id"]
scenario = args["scenario"]
data_mesh = args["data_mesh"]
file_size = args["file_size"]
location = socket.gethostname()

print("({}) Ending benchmark {}_{}_{} run {} at {}".format(
    time.strftime("%H:%M:%S", time.localtime(time.time())),
    scenario, 
    data_mesh, 
    file_size,
    run_id,
    location
))

node_log_file = "/tmp/logs/{}/{}".format(run_id, location)
with open(node_log_file, "r+") as file_object:
    json_data = file_object.read()
    file_object.seek(0)
    node_start = json.loads(json_data)
    
    eth0 = psutil.net_io_counters(pernic=True)["eth0"]
    node_metrics = {
        "start": node_start,
        "end": {
            "timestamp": time.time(),
            "bytes_sent": eth0.bytes_sent,
            "bytes_recv": eth0.bytes_recv,
        }
    }
    json_data = json.dumps(node_metrics)
    file_object.write(json_data)

log_dir = "/tmp/logs/{}/".format(run_id)
interface = Client()
for file_name in os.listdir(log_dir):
    file_path = os.path.join(log_dir, file_name)
    success = interface.upload(file_path)
    if not success:
        raise Exception("Failed to upload file {}".format(file_path))