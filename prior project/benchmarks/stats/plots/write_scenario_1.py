import json
from pathlib import Path

def load_stats(rel_file_path):
    abs_path = Path(rel_file_path).resolve()
    with open(abs_path, "r") as stats_json:
        return json.loads(stats_json.read())

ipfs_stats = load_stats("../calculations/scenarios/scenario_1_ipfs.json")
webdav_stats = load_stats("../calculations/scenarios/scenario_1_webdav.json")

with open("./scenarios/scenario_1_transferred.txt", "w") as file_object:
    for file_size, stats in ipfs_stats.items():
        file_size = int(int(file_size) / 1024)
        mean = stats["total_transmitted"]["mean"]
        stdev = stats["total_transmitted"]["stdev"]
        string = "({}, {}) +- ({}, {}) \n".format(file_size, mean, stdev, stdev)
        file_object.write(string)

    file_object.write("\n")

    for file_size, stats in webdav_stats.items():
        file_size = int(int(file_size) / 1024)
        mean = stats["total_transmitted"]["mean"]
        stdev = stats["total_transmitted"]["stdev"]
        string = "({}, {}) +- ({}, {}) \n".format(file_size, mean, stdev, stdev)
        file_object.write(string)

with open("./scenarios/scenario_1_makespans.txt", "w") as file_object:
    for file_size, stats in ipfs_stats.items():
        file_size = int(int(file_size) / 1024)
        mean = stats["make_span"]["mean"]
        stdev = stats["make_span"]["stdev"]
        string = "({}, {}) +- ({}, {}) \n".format(file_size, mean, stdev, stdev)
        file_object.write(string)

    file_object.write("\n")

    for file_size, stats in webdav_stats.items():
        file_size = int(int(file_size) / 1024)
        mean = stats["make_span"]["mean"]
        stdev = stats["make_span"]["stdev"]
        string = "({}, {}) +- ({}, {}) \n".format(file_size, mean, stdev, stdev)
        file_object.write(string) 

with open("./scenarios/scenario_1_task_times.txt", "w") as file_object:
    for task_key in ["T1", "T2", "T3", "T4", "T5", "T6"]:
        file_object.write("Task {} \n".format(task_key))
        for file_size, stats in ipfs_stats.items():
            file_size = int(int(file_size) / 1024)
            mean = stats["tasks"][task_key]["mean"]
            stdev = stats["tasks"][task_key]["stdev"]
            string = "({}, {}) +- ({}, {}) \n".format(file_size, mean, stdev, stdev)
            file_object.write(string)

        file_object.write("\n")

        for file_size, stats in webdav_stats.items():
            file_size = int(int(file_size) / 1024)
            mean = stats["tasks"][task_key]["mean"]
            stdev = stats["tasks"][task_key]["stdev"]
            string = "({}, {}) +- ({}, {}) \n".format(file_size, mean, stdev, stdev)
            file_object.write(string) 

        file_object.write("\n")