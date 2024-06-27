import os
import json
from pathlib import Path
from statistics import mean, stdev

ipfs_logs = {}
webdav_logs = {}

scenario = "../../results/scenarios/scenario-1/scenario_1_"    
for power in range(10, 32, 2):
    file_size_bytes = 2**power
    extension = str(file_size_bytes) + ".json"
    ipfs_path = str(Path(scenario + "ipfs_" + extension).resolve())
    webdav_path = str(Path(scenario + "webdav_" + extension).resolve())

    if os.path.isfile(ipfs_path):
        with open(ipfs_path, "r") as file_object:
            log_data = file_object.read()
            json_data = json.loads(log_data)
            ipfs_logs[file_size_bytes] = json_data[-10:]

    if os.path.isfile(webdav_path):
        with open(webdav_path, "r") as file_object:
            log_data = file_object.read()
            json_data = json.loads(log_data)
            webdav_logs[file_size_bytes] = json_data[-10:]

def calculate_task_averages(run_logs):
    task_averages = {}
    for task_key in ["T1", "T2", "T3", "T4", "T5", "T6"]:  
        times = []

        for run_log in run_logs:
            start_time = run_log["tasks"][task_key]["time_start"]

            end_time = None
            if task_key in ["T2", "T4", "T6"]:
                end_time = run_log["tasks"][task_key]["time_read"]
            else:
                end_time = run_log["tasks"][task_key]["time_upload"]

            times.append(end_time - start_time)

        task_averages[task_key] = {
            "min": min(times),
            "mean": mean(times),
            "max": max(times),
            "stdev": stdev(times),
        }

    return task_averages


def calculate_make_span(task_log):
    total_time = 0
    total_time += task_log["T1"]["time_upload"] - task_log["T1"]["time_start"]
    total_time += task_log["T2"]["time_read"] - task_log["T2"]["time_start"]
    total_time += task_log["T3"]["time_upload"] - task_log["T3"]["time_start"]
    total_time += task_log["T4"]["time_read"] - task_log["T4"]["time_start"]
    total_time += task_log["T5"]["time_upload"] - task_log["T5"]["time_start"]
    total_time += task_log["T6"]["time_read"] - task_log["T6"]["time_start"]
    return total_time

def node_total_transmitted(node_log, node):
    total_bytes = 0
    total_bytes += node_log[node]["end"]["bytes_sent"] - node_log[node]["start"]["bytes_sent"]
    total_bytes += node_log[node]["end"]["bytes_recv"] - node_log[node]["start"]["bytes_recv"]
    return total_bytes

def calculate_total_mb_transmitted(node_log):
    total_bytes = 0
    total_bytes += node_total_transmitted(node_log, "dm1")
    total_bytes += node_total_transmitted(node_log, "dm2")
    total_bytes += node_total_transmitted(node_log, "dm3")
    total_bytes += node_total_transmitted(node_log, "dm4")
    return int(total_bytes / (1024 * 1024))

def calculate_stats(logs):
    stats = {}
    
    for key, value in logs.items():
        stats[key] = {}

        stats[key]["tasks"] = calculate_task_averages(value)

        make_span_list = []
        for size_log in value:
            task_log = size_log["tasks"]
            make_span = calculate_make_span(task_log)
            make_span_list.append(make_span)

        total_transmitted_list = []
        for size_log in value:
            node_log = size_log["nodes"]
            total_transmitted = calculate_total_mb_transmitted(node_log)
            total_transmitted_list.append(total_transmitted)
        
        stats[key]["make_span"] = {
            "min": min(make_span_list),
            "mean": mean(make_span_list),
            "max": max(make_span_list),
            "stdev": stdev(make_span_list)
        }
        stats[key]["total_transmitted"] = {
            "min": min(total_transmitted_list),
            "mean": mean(total_transmitted_list),
            "max": max(total_transmitted_list),
            "stdev": stdev(total_transmitted_list),
        }
    return stats

st = calculate_stats(ipfs_logs)
for size, stat in st.items():
    print("{} +- {}".format(stat["make_span"]["mean"], stat["make_span"]["stdev"]))

# with open("./scenarios/scenario_1_ipfs.json", "w") as file_object:
#     stats = calculate_stats(ipfs_logs)
#     json_data = json.dumps(stats, indent=4)
#     file_object.write(json_data)
# with open("./scenarios/scenario_1_webdav.json", "w") as file_object:
#     stats = calculate_stats(webdav_logs)
#     json_data = json.dumps(stats, indent=4)
#     file_object.write(json_data)