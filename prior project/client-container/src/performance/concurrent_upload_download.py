import os
import gc
import time
from timeit import default_timer as timer

from multiprocessing.connection import Listener
from multiprocessing.connection import Client as ClientSocket

from util_files import create_file

from client import Client

is_coordinator = os.environ.get("IS_COORDINATOR")

start_time = 0

if is_coordinator is not None:
    start_time = time.time() + 6
    print("start_timeing at " + str(start_time))

    client_count = int(os.environ["CLIENT_COUNT"])

    listener = Listener(("0.0.0.0", 12000))

    for client_number in range(client_count):
        connection = listener.accept()
        print("Client: " + str(client_number) + " connected")
        connection.send(start_time)
        connection.close()
    
else:
    print("Waiting for coordinator to start_timeup...")
    time.sleep(3)
    connection = ClientSocket(("coordinator", 12000))
    start_time = connection.recv()
    print("Received start_time time: " + str(start_time))


print("Waiting to begin...")
while time.time() < start_time:
    time.sleep(0.1)

print("Beginning...")

interface = Client()
container_id = os.environ["CONTAINER_ID"]

print("Creating files")
file_paths = []
for file_id in range(10):
    file_path = "/tmp/file_" + container_id + "_" + str(file_id)
    file_paths.append(create_file(1024, file_path))

start_begin = timer()

print("start_timeing uploads")
for file_path in file_paths:
    interface.upload(file_path)

print("start_timeing downloads")
for file_path in file_paths:
    interface.download(file_path)

start_end = timer()
print("Duration: " + str(start_end - start_begin))