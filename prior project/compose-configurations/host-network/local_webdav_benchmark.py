from benchmark_runner import docker_pull, docker_compose_run
from benchmark_parameters import file_sizes, run_count, interval_seconds

docker_pull(container="nicoja/webdav-service2", output_file="/tmp/webdav-service2.log")
docker_pull(container="nicoja/client-container", output_file="/tmp/client-container.log")

for file_size_name, file_size in file_sizes.items():
    environment = {
        "SCRIPT": "local_webdav_read.py",
        "FILE_SIZE": str(file_size),
        "RUN_COUNT": str(run_count),
        "INTERVAL_SECONDS": str(interval_seconds),
    }

    docker_compose_run (
        compose_file="/tmp/local_webdav_setup.yml",
        output_file="/tmp/logs/local_webdav_read_" + file_size_name + ".log",
        environment=environment,
    )

for file_size_name, file_size in file_sizes.items():
    environment = {
        "SCRIPT": "local_webdav_write.py",
        "FILE_SIZE": str(file_size),
        "RUN_COUNT": str(run_count),
        "INTERVAL_SECONDS": str(interval_seconds),
    }

    docker_compose_run (
        compose_file="/tmp/local_webdav_setup.yml",
        output_file="/tmp/logs/local_webdav_write_" + file_size_name + ".log",
        environment=environment,
    )