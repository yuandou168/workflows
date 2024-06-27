import sys
import psutil
import socket
import time
from threading import Thread, Lock
from multiprocessing.connection import Client, Listener

master_address = sys.argv[1]
print("Master address is {}".format(master_address))

worker_address = psutil.net_if_addrs()["eth0"][0].address
print("My address is {}".format(worker_address))

worker_connections = []

hostname = socket.gethostname()
worker_metrics = {"name": hostname}
print("My hostname is {}".format(hostname))

task_logs = []
task_logs_lock = Lock()

def accept_workers():
    master_listener = Listener(address=("0.0.0.0", 20000))
    print("Listening for worker connections")

    while True:
        new_worker = master_listener.accept()
        print("New worker connected")
        worker_connections.append(new_worker)

def connect_to_master():
    master_connection = None
    while master_connection is None:
        try:
            master_connection = Client(address=(master_address, 20000))
            print("Connected to master")

            try:
                while True:
                    master_command = master_connection.recv()

                    task_logs_lock.acquire()
                    
                    if master_command == "start":
                        print("Received start from master")
                        eth0 = psutil.net_io_counters(pernic=True)["eth0"]
                        worker_metrics["start"] = {
                            "timestamp": time.time(),
                            "bytes_sent": eth0.bytes_sent,
                            "bytes_recv": eth0.bytes_recv          
                        }
                        task_logs = []
                    elif master_command == "end":
                        print("Received end from master")
                        eth0 = psutil.net_io_counters(pernic=True)["eth0"]
                        worker_metrics["end"] = {
                            "timestamp": time.time(),
                            "bytes_sent": eth0.bytes_sent,
                            "bytes_recv": eth0.bytes_recv          
                        }
                        print(task_logs)
                        master_connection.send(worker_metrics)
                        master_connection.send(task_logs)
                        print("Send metrics and task logs to master")
                        master_connection.recv()
                        print("Data has been received")
                        task_logs = []

                    task_logs_lock.release()
            except:
                print("Error communicating with master...")
                master_connection = None
        except:
            print("Could not connect to master...")
            time.sleep(1)

def listen_for_benchmark():
    benchmark_listener = Listener(address=("127.0.0.1", 21000))

    while True:
        benchmark_connection = benchmark_listener.accept()
        print("New benchmark connection")
        benchmark_command = benchmark_connection.recv()

        if benchmark_command == "start":
            print("Benchmark connection issued start")

            for worker_connection in worker_connections:
                print("Sending start to worker")
                worker_connection.send("start")

            benchmark_connection.send(True)

        elif benchmark_command == "end":
            print("Benchmark connection issued end")
            combined_metrics_list = []
            combined_task_logs = []

            for worker_connection in worker_connections:
                print("Sending end to worker")
                worker_connection.send("end")

                worker_metrics = worker_connection.recv()
                worker_task_log = worker_connection.recv()
                print("Received metrics and task logs from worker")

                worker_connection.send(True)
                print("Send acknowledge to worker")

                combined_metrics_list.append(worker_metrics)
                combined_task_logs.extend(worker_task_log)

            benchmark_connection.send(combined_metrics_list)
            benchmark_connection.send(combined_task_logs)
            print("Send combined metrics and combined task logs")

if master_address == worker_address:
    accept_workers_thread = Thread(target=accept_workers)
    accept_workers_thread.start()

    listen_for_benchmark_thread = Thread(target=listen_for_benchmark)
    listen_for_benchmark_thread.start()

connect_to_master_thread = Thread(target=connect_to_master)
connect_to_master_thread.start()

## REMOVE IN FAVOUR OF DISK LOG
def listen_for_tasks():
    task_listener = Listener(("127.0.0.1", 22000))

    while True:
        new_task_connection = task_listener.accept()
        print("New task connected")

        logs = new_task_connection.recv()
        print("Received logs from task")

        task_logs_lock.acquire()
        task_logs.append(logs)
        task_logs_lock.release()

listen_for_tasks_thread = Thread(target=listen_for_tasks)
listen_for_tasks_thread.start()
