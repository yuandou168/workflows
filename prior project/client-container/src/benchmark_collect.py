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
tasks = args["tasks"]
dms = args["dms"]
location = socket.gethostname()

print("({}) Collecting results of benchmark {}_{}_{} run {} at {}".format(
    time.strftime("%H:%M:%S", time.localtime(time.time())),
    scenario, 
    data_mesh, 
    file_size,
    run_id,
    location
))

node_logs = {}
task_logs = {}

log_dir = "/tmp/logs/{}/".format(run_id)
interface = Client()
for task in tasks:
    task_log_file = log_dir + task

    success = False
    attempts = 0
    while not success:
        success = interface.download(task_log_file)

        if not success:
            attempts += 1
        if attempts > 10000:
            raise Exception("Failed to download file {}".format(task_log_file))
    
    with open(task_log_file, "r") as file_object:
        json_data = file_object.read()
        log = json.loads(json_data)
        task_logs[task] = log

for dm in dms:
    dm_log_file = log_dir + dm

    success = False
    attempts = 0
    while not success:
        success = interface.download(dm_log_file)

        if not success:
            attempts += 1
        if attempts > 10000:
            raise Exception("Failed to download file {}".format(dm_log_file))

    with open(dm_log_file, "r") as file_object:
        json_data = file_object.read()
        log = json.loads(json_data)
        node_logs[dm] = log

# total_bytes_sent = 0
# total_bytes_recv = 0
# for dm, node_log in node_logs.items():
#     start_bytes_sent = node_log["start"]["bytes_sent"]
#     end_bytes_sent = node_log["end"]["bytes_sent"]
#     total_bytes_sent += end_bytes_sent - start_bytes_sent

#     start_bytes_recv = node_log["start"]["bytes_recv"]
#     end_bytes_recv = node_log["end"]["bytes_recv"]
#     total_bytes_recv += end_bytes_recv - start_bytes_recv

# print("Total MB sent: {}".format(total_bytes_sent / (1024 * 1024)))
# print("Total MB received: {}".format(total_bytes_recv / (1024 * 1024)))

final_log_file = "/tmp/{}_{}_{}.json".format(scenario, data_mesh, file_size)
print("({}) Inserting into final log file {}".format(
    time.strftime("%H:%M:%S", time.localtime(time.time())),
    final_log_file
))

if not os.path.exists(final_log_file):
    open(final_log_file, "w").close()

with open(final_log_file, "r+") as file_object:
    log_object = {
        "nodes": node_logs,
        "tasks": task_logs,
    }

    log_object_list = None

    try:
        json_data = file_object.read()
        log_object_list = json.loads(json_data)
        file_object.seek(0)
        log_object_list.append(log_object)
    except:
        log_object_list = [log_object]
    
    json_data = json.dumps(log_object_list, indent=4)
    file_object.write(json_data)
    file_object.truncate()