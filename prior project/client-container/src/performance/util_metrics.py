import psutil
import gc
import time
from timeit import default_timer as timer
import datetime

# gc.disable()

def log_metrics():
    row = list(range(18))
    
    row[0] = timer()
    row[1] = time.time()

    cpu = psutil.cpu_times(percpu=False)
    row[2] = cpu.user
    row[3] = cpu.system
    row[4] = cpu.idle
    if hasattr(cpu, "iowait"):
        row[5] = cpu.iowait

    disk = psutil.disk_io_counters(perdisk=False)
    row[6] = disk.read_bytes
    row[7] = disk.write_bytes
    row[8] = disk.read_count
    row[9] = disk.write_count

    mem = psutil.virtual_memory()
    row[10] = mem.available
    row[11] = mem.used
    row[12] = mem.free
    if hasattr(mem, "cached"):
        row[13] = mem.cached

    net = psutil.net_io_counters(pernic=True)
    if "lo" in net:
        lo = net["lo"]
        row[14] = lo.bytes_sent
        row[15] = lo.bytes_recv
    if "eth0" in net:
        eth_0 = net["eth0"]
        row[16] = eth_0.bytes_sent
        row[17] = eth_0.bytes_recv
    
    return row 

def log_event(event):
    print(datetime.datetime.now().strftime("%H:%M.%S") + ": " + event)

# metric_names = [
#     "time",

#     "cpu.user",
#     "cpu.system",
#     "cpu.idle",
#     "cpu.iowait",

#     "disk.read_bytes",
#     "disk.write_bytes",
#     "disk.read_count",
#     "disk.write_count",

#     "mem.available",
#     "mem.used",
#     "mem.free",
#     "mem.cached",

#     "lo.bytes_sent",
#     "lo.bytes_recv",
#     "eth0.bytes_sent",
#     "eth0.bytes_recv",
# ]

# file_sizes = None
# if os.environ.get("DEBUG") != None:
#     run_count = 1
#     interval_time = 0.5
#     file_sizes = {
#         "1KB": 2 ** 10,
#         "4KB": 2 ** 12,
#     }
# else:
#     run_count = 15
#     interval_time = 60
#     file_sizes = {
#         # "1KB": 2 ** 10,
#         # "4KB": 2 ** 12,
#         # "16KB": 2 ** 14,
#         # "64KB": 2 ** 16,
#         # "256KB": 2 ** 18,
#         # "1MB": 2 ** 20,
#         # "4MB": 2 ** 22,
#         # "16MB": 2 ** 24, 
#         # "64MB": 2 ** 26,
#         "256MB": 2 ** 28,
#         "1024MB": 2 ** 30,
#     }

# def get_file_size_name(number_of_bytes):
#     to_MB = number_of_bytes / (1024 * 1024)
#     if to_MB.is_integer():
#         return str(int(to_MB)) + "MB"
#     else:
#         return str(int(file_size / 1024)) + "KB"