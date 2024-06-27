import os
import subprocess
import platform
import datetime

def docker_pull(container, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    file_object = open(output_file, "w")
    pull_process = subprocess.Popen([
        "docker", "pull", container
        ], stdout=file_object, stderr=file_object)
    file_object.close()
    pull_process.wait()

def docker_compose_run(compose_file, output_file, environment, call_back=None):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    time_start = datetime.datetime.now()

    prune_containers = "echo y | docker container prune"
    setup = "docker-compose --no-ansi --file " + compose_file + " up --abort-on-container-exit"
    teardown = "docker-compose --no-ansi --file " + compose_file + " down"
    prune_volumes = "echo y | docker volume prune"
    process = subprocess.Popen(
        args="{}; {}; {}; {};".format(prune_containers, setup, teardown, prune_volumes), 
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        close_fds=True,
        shell=True,
    )

    if call_back is not None:
        call_back()

    stdout, _ = process.communicate()

    time_end = datetime.datetime.now()

    file_object = open(output_file, "w")

    file_object.write("Time start: " + time_start.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    file_object.write("Time end: " + time_end.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    file_object.write("Duration: " + str(time_end - time_start) + "\n")

    file_object.write("\n")

    file_object.write("Platform: " + platform.platform() + "\n")
    file_object.write("Name: " + platform.uname().node + "\n")
    file_object.write("Release: " + platform.uname().version + "\n")

    file_object.write("\n")

    file_object.write("Compose file: " + compose_file + "\n")
    file_object.write("Script: " + environment["SCRIPT"] + "\n")
    file_object.write("Environment vars:\n")
    for key, value in environment.items():
        file_object.write(key + ": " + value + "\n")
    file_object.write("\n")

    file_object.write(stdout.decode("utf-8"))
    file_object.close()

def docker_compose_run_daemon(compose_file):
    prune_process = subprocess.Popen(["echo", "y", "|" , "docker", "container", "prune"])
    prune_process.wait()

    return subprocess.Popen(["docker-compose", "--file", compose_file, "up", "--abort-on-container-exit"])

def docker_compose_kill_daemon(compose_file, daemon):
    daemon.kill()
    daemon.wait()
    
    down_process = subprocess.Popen(["docker-compose", "--file", compose_file, "down"])
    down_process.wait()

    prune_process = subprocess.Popen(["echo", "y", "|", "docker", "volume", "prune"])
    prune_process.wait()

print("Pulling client-container")
docker_pull(container="nicoja/client-container", output_file="/tmp/client-container.log")

print("Pulling ipfs")
docker_pull(container="nicoja/ipfs-node", output_file="/tmp/ipfs-node.log")
docker_pull(container="nicoja/ipfs-service2", output_file="/tmp/ipfs-service2.log")

print("Pulling webdav")
docker_pull (container="bytemark/webdav:2.4", output_file="/tmp/webdav.log")
docker_pull(container="nicoja/webdav-service2", output_file="/tmp/webdav-service.log")

print("Done")