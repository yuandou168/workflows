import os

def get_file_size_name(number_of_bytes):
    to_MB = number_of_bytes / (1024 * 1024)
    if to_MB.is_integer():
        return str(int(to_MB)) + "MB"
    else:
        return str(int(number_of_bytes / 1024)) + "KB"

protocol = os.environ.get("PROTOCOL")
file_size = int(os.environ.get("FILE_SIZE"))
file_size_name = get_file_size_name(file_size)
run_count = int(os.environ.get("RUN_COUNT"))
interval_seconds = float(os.environ.get("INTERVAL_SECONDS"))