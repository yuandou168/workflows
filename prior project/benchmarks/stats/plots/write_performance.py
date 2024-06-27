import json
from pathlib import Path

def load_stats(rel_file_path):
    abs_path = Path(rel_file_path).resolve()
    with open(abs_path, "r") as stats_json:
        return json.loads(stats_json.read())

def print_stats(stats, points, metric, adjust):
    strings = []

    for point in points:
        
        strings.append(point)

        file_size_exp = 10
        for file_size_name in stats.keys():
            metric_stats = stats[file_size_name][point][metric]

            file_size = int((2**file_size_exp) / 1024)
            file_size_exp += 2

            mean = adjust(metric_stats["mean"])
            stdev = adjust(metric_stats["stdev"])

            strings.append("({}, {}) +- ({}, {})".format(file_size, mean, stdev, stdev))

        strings.append("")

    return strings

def write_stats(rel_file_path, points, metric, adjust, output_file):
    stats = load_stats(rel_file_path)
    strings = print_stats(stats, points, metric, adjust)

    with open(output_file, "w") as output:
        for string in strings:
            output.write(string + "\n")

def disk_read_write():
    write_stats(
        rel_file_path="../calculations/performance/read-write/disk_read.json",
        points=["1-2"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/read-write/disk_read_time.txt",
    )
    write_stats(
        rel_file_path="../calculations/performance/read-write/disk_write.json",
        points=["1-2"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/read-write/disk_write_time.txt",
    )

def ipfs_read_write():
    write_stats(
        rel_file_path="../calculations/performance/read-write/ipfs_read.json",
        points=["1-8", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/read-write/ipfs_read_time.txt",
    )
    write_stats(
        rel_file_path="../calculations/performance/read-write/ipfs_write.json",
        points=["1-9", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8", "8-9"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/read-write/ipfs_write_time.txt",
    )
  

def webdav_read_write():
    write_stats(
        rel_file_path="../calculations/performance/read-write/webdav_read.json",
        points=["1-5", "1-2", "2-3", "3-4", "4-5"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/read-write/webdav_read_time.txt",
    )
    write_stats(
        rel_file_path="../calculations/performance/read-write/webdav_write.json",
        points=["1-6", "1-2", "2-3", "3-4", "4-5", "5-6"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/read-write/webdav_write_time.txt",
    )

def read_write():
    disk_read_write()
    ipfs_read_write()
    webdav_read_write()

def ftp_download_upload():
    write_stats(
        rel_file_path="../calculations/performance/download-upload/ftp_download.json",
        points=["1-2"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/download-upload/ftp_download_time.txt",
    )
    write_stats(
        rel_file_path="../calculations/performance/download-upload/ftp_download.json",
        points=["1-2"],
        metric="eth0.bytes_recv/s",
        adjust= lambda m: m / 1024,
        output_file="./performance/download-upload/ftp_download_throughput.txt",
    )

    write_stats(
        rel_file_path="../calculations/performance/download-upload/ftp_upload.json",
        points=["1-2"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/download-upload/ftp_upload_time.txt",
    )
    write_stats(
        rel_file_path="../calculations/performance/download-upload/ftp_upload.json",
        points=["1-2"],
        metric="eth0.bytes_sent/s",
        adjust= lambda m: m / 1024,
        output_file="./performance/download-upload/ftp_upload_throughput.txt",
    )

def ipfs_download_upload():
    write_stats(
        rel_file_path="../calculations/performance/download-upload/ipfs_download.json",
        points=["1-7", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/download-upload/ipfs_download_time.txt",
    )
    write_stats(
        rel_file_path="../calculations/performance/download-upload/ipfs_download.json",
        points=["1-7", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7"],
        metric="eth0.bytes_recv/s",
        adjust= lambda m: m / 1024,
        output_file="./performance/download-upload/ipfs_download_throughput.txt",
    )

    write_stats(
        rel_file_path="../calculations/performance/download-upload/ipfs_upload.json",
        points=["1-8", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/download-upload/ipfs_upload_time.txt",
    )
    write_stats(
        rel_file_path="../calculations/performance/download-upload/ipfs_upload.json",
        points=["1-8", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8"],
        metric="eth0.bytes_sent/s",
        adjust= lambda m: m / 1024,
        output_file="./performance/download-upload/ipfs_upload_throughput.txt",
    )

def webdav_download_upload():
    write_stats(
        rel_file_path="../calculations/performance/download-upload/webdav_download.json",
        points=["1-4", "1-2", "2-3", "3-4"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/download-upload/webdav_download_time.txt",
    )
    write_stats(
        rel_file_path="../calculations/performance/download-upload/webdav_download.json",
        points=["1-4", "1-2", "2-3", "3-4"],
        metric="eth0.bytes_recv/s",
        adjust= lambda m: m / 1024,
        output_file="./performance/download-upload/webdav_download_throughput.txt",
    )

    write_stats(
        rel_file_path="../calculations/performance/download-upload/webdav_upload.json",
        points=["1-5", "1-2", "2-3", "3-4", "4-5"],
        metric="timer",
        adjust= lambda m: m * 1000,
        output_file="./performance/download-upload/webdav_upload_time.txt",
    )
    write_stats(
        rel_file_path="../calculations/performance/download-upload/webdav_upload.json",
        points=["1-5", "1-2", "2-3", "3-4", "4-5"],
        metric="eth0.bytes_sent/s",
        adjust= lambda m: m / 1024,
        output_file="./performance/download-upload/webdav_upload_throughput.txt",
    )

def download_upload():
    ftp_download_upload()
    ipfs_download_upload()
    webdav_download_upload()

def main():
    print("Plots start!")
    
if __name__=="__main__": 
    main()
    read_write()
    download_upload()