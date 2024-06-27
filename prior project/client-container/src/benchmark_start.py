import os
import sys
import json
import time
import socket
import psutil

args = json.loads(sys.argv[1])
run_id = args["run_id"]
scenario = args["scenario"]
data_mesh = args["data_mesh"]
file_size = args["file_size"]
location = socket.gethostname()

print("({}) Starting benchmark {}_{}_{} run {} at {}".format(
    time.strftime("%H:%M:%S", time.localtime(time.time())),
    scenario, 
    data_mesh,
    file_size,
    run_id,
    location
))

os.makedirs("/tmp/data/", exist_ok=True)
for root, dirs, files in os.walk("/tmp/data/"):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

os.makedirs("/tmp/logs/{}/".format(run_id), exist_ok=True)
for root, dirs, files in os.walk("/tmp/logs/{}/".format(run_id)):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

node_log_file = "/tmp/logs/{}/{}".format(run_id, location)
with open(node_log_file, "w") as file_object:
    eth0 = psutil.net_io_counters(pernic=True)["eth0"]
    node_start = {
        "timestamp": time.time(),
        "bytes_sent": eth0.bytes_sent,
        "bytes_recv": eth0.bytes_recv    
    }
    json_data = json.dumps(node_start)
    file_object.write(json_data)