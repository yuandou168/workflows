from benchmark_runner import docker_pull, docker_compose_run
from benchmark_parameters import file_sizes, run_count, interval_seconds

docker_pull(container="nicoja/ipfs-node", output_file="/tmp/ipfs-node.log")
docker_pull(container="nicoja/ipfs-service2", output_file="/tmp/ipfs-service2.log")
docker_pull(container="nicoja/client-container", output_file="/tmp/client-container.log")

for file_size_name, file_size in file_sizes.items():
    environment = {
        "SCRIPT": "performance/local_ipfs_read.py",
        "FILE_SIZE": str(file_size),
        "RUN_COUNT": str(run_count),
        "INTERVAL_SECONDS": str(interval_seconds),
    }

    docker_compose_run (
        compose_file="local_ipfs_setup.yml",
        output_file="/tmp/logs/local_ipfs_read_" + file_size_name + ".log",
        environment=environment,
    )

for file_size_name, file_size in file_sizes.items():
    environment = {
        "SCRIPT": "performance/local_ipfs_write.py",
        "FILE_SIZE": str(file_size),
        "RUN_COUNT": str(run_count),
        "INTERVAL_SECONDS": str(interval_seconds),
    }

    docker_compose_run (
        compose_file="local_ipfs_setup.yml",
        output_file="/tmp/logs/local_ipfs_write_" + file_size_name + ".log",
        environment=environment,
    )