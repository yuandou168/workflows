import os
import json
import fnmatch
from pathlib import Path
from statistics import mean, stdev

metric_names = [
    "timer",                #0
    "timestamp",            #1

    "cpu.user",             #2
    "cpu.system",           #3
    "cpu.idle",             #4
    "cpu.iowait",           #5

    "disk.read_bytes",      #6
    "disk.write_bytes",     #7
    "disk.read_count",      #8
    "disk.write_count",     #9

    "mem.available",        #10
    "mem.used",             #11
    "mem.free",             #12
    "mem.cached",           #13

    "lo.bytes_sent",        #14
    "lo.bytes_recv",        #15
    "eth0.bytes_sent",      #16
    "eth0.bytes_recv",      #17

    "lo.bytes_sent/s",      #18
    "lo.bytes_recv/s",      #19
    "eth0.bytes_sent/s",    #20
    "eth0.bytes_recv/s",    #21
]

# Get json files from a directory, returns a list with (file_size_name, absolute_file_path)
def get_json_files(rel_in_dir, pattern):
    dir_files = os.listdir(rel_in_dir)
    
    filtered = fnmatch.filter(dir_files, pattern)

    # Sort by KB < MB, then numerical size
    filtered = sorted(filtered, key=lambda file_path: (file_path.split("_")[-1:][0].split(".")[:-1][0][-2:], int(file_path.split("_")[-1:][0].split(".")[:-1][0][:-2])))

    abs_dir = str(Path(rel_in_dir).resolve())
    json_files = []
    for file_name in filtered:
        file_size_name = file_name.split(".")[0].split("_")[-1:][0]
        absolute_file_path = abs_dir + "/" + file_name
        json_files.append((file_size_name, absolute_file_path))

    return json_files

# Returns a list of lists where each list is the difference between two recorded points of a metric
def aggregate_metrics(runs, point_1, point_2):
    metrics_lists = list(range(len(metric_names)))
    for metric in metrics_lists:
        metrics_lists[metric] = []

    for run_id in range(2, len(runs)):
        run = runs[run_id]

        # Retrieve the metrics recorded at the specified point
        point_1_metrics = run[point_1]        
        point_2_metrics = run[point_2]

        # Timestamp was not logged in some parts, add default value of 0
        if len(point_1_metrics) != 18:
            point_1_metric.insert(1, 0)
        if len(point_2_metrics) != 18:
            point_2_metrics.insert(1, 0)

        # Subtract point 1 from point 2 for total incrementing counters
        for metric_index in range(18):
            point_1_metric = point_1_metrics[metric_index]
            point_2_metric = point_2_metrics[metric_index]

            difference = point_2_metric - point_1_metric
            metrics_lists[metric_index].append(difference)

        # Add throughput by dividing bytes sent/received during that time by the time in seconds
        time_diff = point_2_metrics[0] - point_1_metrics[0]
        metrics_lists[18].append((point_2_metrics[14] - point_1_metrics[14]) / time_diff)
        metrics_lists[19].append((point_2_metrics[15] - point_1_metrics[15]) / time_diff)
        metrics_lists[20].append((point_2_metrics[16] - point_1_metrics[16]) / time_diff)
        metrics_lists[21].append((point_2_metrics[17] - point_1_metrics[17]) / time_diff)

    return metrics_lists

# Calculates stats from the list of aggregated metrics differences
def calculate_metrics_statistics(metrics_lists):
    metric_stats = {}

    for metric_index in range(len(metric_names)):
        metric_name = metric_names[metric_index]
        metric_values = metrics_lists[metric_index]
        print("metric_values", metric_values)

        metric_stats[metric_name] = {
            "minimum": min(metric_values),
            "mean": mean(metric_values),
            "maximum": max(metric_values),
            "stdev": stdev(metric_values),
        }

    return metric_stats

# Calculate stats for each point point_1-point_2 in points
def calculate_points_stats(runs, points):
    stats = {}

    for point in points:
        (point_1, point_2) = tuple(point.split("-"))

        metrics_lists = aggregate_metrics(runs=runs, point_1=point_1, point_2=point_2)
        metric_stats = calculate_metrics_statistics(metrics_lists)
        stats[point_1 + "-" + point_2] = metric_stats

    return stats

def load_runs(file_path):
    with open(file_path, "r") as json_file:
        return json.loads(json_file.read())

def save_stats(data, output_path):
    with open(output_path, "w") as json_output:
        json_output.write(json.dumps(data, indent=4))

# Final function: calculates stats for each file size and aggregates it into a single json file
def calculate_stats(rel_in_dir, pattern, points, output_file):
    json_files = get_json_files(rel_in_dir=rel_in_dir, pattern=pattern)
    
    complete_statistics = {}

    for file_size_name, abs_file_path in json_files:
        runs = load_runs(abs_file_path)
        points_stats = calculate_points_stats(runs=runs, points=points) 

        complete_statistics[file_size_name] = points_stats
        # print("xxx", runs)
    save_stats(complete_statistics, output_file)

def disk_read_write():
    calculate_stats(
        rel_in_dir="../../results/performance/read-write/disk/", 
        pattern="local_disk_read_*.json", 
        points=["1-2"],
        output_file="./performance/read-write/disk_read.json",
    )
    calculate_stats(
        rel_in_dir="../../results/performance/read-write/disk/", 
        pattern="local_disk_write_*.json", 
        points=["1-2"],
        output_file="./performance/read-write/disk_write.json",
    )

def ipfs_read_write():
    calculate_stats(
        rel_in_dir="../../results/performance/read-write/ipfs/", 
        pattern="local_ipfs_read_*.json", 
        points=["1-8", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8"],
        output_file="./performance/read-write/ipfs_read.json",
    )
    calculate_stats(
        rel_in_dir="../../results/performance/read-write/ipfs/", 
        pattern="local_ipfs_write_*.json", 
        points=["1-9", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8", "8-9"],
        output_file="./performance/read-write/ipfs_write.json",
    )

def webdav_read_write():
    calculate_stats(
        rel_in_dir="../../results/performance/read-write/webdav/", 
        pattern="local_webdav_read_*.json",
        points=["1-5", "1-2", "2-3", "3-4", "4-5"],
        output_file="./performance/read-write/webdav_read.json",
    )
    calculate_stats(
        rel_in_dir="../../results/performance/read-write/webdav/", 
        pattern="local_webdav_write_*.json", 
        points=["1-6", "1-2", "2-3", "3-4", "4-5", "5-6"],
        output_file="./performance/read-write/webdav_write.json",
    )

def all_read_write():
    disk_read_write()
    ipfs_read_write()
    webdav_read_write()

# FTP
# para: vm pairs, e.g., v1s-v2c
def ftp_download_upload(vm_pair):
    path = "/Users/y.wang8uva.nl/experiments2021-2024/Benchmarks/"
    calculate_stats(
        # rel_in_dir="../../results/performance/download-upload/ftp/", 
        rel_in_dir=path+"performance/download-upload/FTP/publicIP/" + vm_pair + "/logs/",
        pattern="transfer_ftp_download_*.json", 
        points=["1-2"],
        output_file=path+"stats/calculations/performance_stats/download-upload/FTP/publicIP/" + vm_pair + "/ftp_download.json", 
    )
    calculate_stats(
        rel_in_dir=path+"performance/download-upload/FTP/publicIP/" + vm_pair + "/logs/", 
        pattern="transfer_ftp_upload_*.json", 
        points=["1-2"],
        output_file=path+"stats/calculations/performance_stats/download-upload/FTP/publicIP/" + vm_pair + "/ftp_upload.json",
    )

# IPFS
def ipfs_download_upload(vm_pair):
    path = "/Users/y.wang8uva.nl/experiments2021-2024/Benchmarks/"
    calculate_stats(
        # rel_in_dir="../../results/performance/download-upload/ipfs/", 
        rel_in_dir=path+"performance/download-upload/IPFS/publicIP/" + vm_pair + "/logs/",
        pattern="transfer_ipfs_download_*.json", 
        points=["1-7", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7"],
        # output_file="./performance/download-upload/ipfs_download.json",
        output_file=path+"stats/calculations/performance_stats/download-upload/IPFS/publicIP/" + vm_pair + "/ipfs_download.json", 
    )
    calculate_stats(
        rel_in_dir=path+"performance/download-upload/IPFS/publicIP/" + vm_pair + "/logs/",
        pattern="transfer_ipfs_upload_*.json", 
        points=["1-8", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8"],
        output_file=path+"stats/calculations/performance_stats/download-upload/IPFS/publicIP/" + vm_pair + "/ipfs_upload.json", 
        # output_file="./performance/download-upload/ipfs_upload.json",
    )

# WebDAV
def webdav_download_upload(vm_pair):
    path = "/Users/y.wang8uva.nl/experiments2021-2024/Benchmarks/"
    calculate_stats(
        # rel_in_dir="../../results/performance/download-upload/webdav/", 
        rel_in_dir=path+"performance/download-upload/WebDAV/publicIP/" + vm_pair + "/logs/",
        pattern="transfer_webdav_download_*.json", 
        points=["1-4", "1-2", "2-3", "3-4"],
        # output_file="./performance/download-upload/webdav_download.json",
        output_file=path+"stats/calculations/performance_stats/download-upload/WebDAV/publicIP/" + vm_pair + "/webdav_download.json", 
    )
    calculate_stats(
        # rel_in_dir="../../results/performance/download-upload/webdav/", 
        rel_in_dir=path+"performance/download-upload/WebDAV/publicIP/" + vm_pair + "/logs/",
        pattern="transfer_webdav_upload_*.json", 
        points=["1-5", "1-2", "2-3", "3-4", "4-5"],
        # output_file="./performance/download-upload/webdav_upload.json",
        output_file=path+"stats/calculations/performance_stats/download-upload/WebDAV/publicIP/" + vm_pair + "/webdav_upload.json", 
    )

def all_download_upload():
    ftp_download_upload()
    ipfs_download_upload()
    webdav_download_upload()

if __name__ == "__main__":
    # vm_pairs = ["v1s-v2c", "v1s-v3c", "v1s-v4c", "v2s-v3c", "v2s-v4c", "v3s-v4c"]
    ftp_download_upload("v2-v4")
    # ipfs_download_upload("v2-v3")
    # webdav_download_upload("v2-v3")