import json
import os

def create_bytes(byte_count):
    return os.urandom(byte_count)

def create_file(file_size, file_path):
    os.makedirs(os.path.dirname("/tmp/files/"), exist_ok=True)

    byte_array = create_bytes(file_size)

    with open(file_path, "wb") as out:
        out.write(byte_array)

    return file_path

def delete_file(file_path):
    os.remove(file_path)

def write_json(file_name, json_data):
    os.makedirs(os.path.dirname("/tmp/logs/"), exist_ok=True)
    with open("/tmp/logs/" + file_name + ".json", "w") as jsonfile:
        json.dump(json_data, jsonfile, indent=4, sort_keys=True)