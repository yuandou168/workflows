from laserfarm import Retiler
import sys
import json
import os
from log_util import log_now

# Start
log_start = log_now()

# Finished download
log_download = log_now()

input_file = sys.argv[1]
pipeline = Retiler(input_file=input_file)
input_dict = {
    'set_grid': {
        'min_x': -113107.81,
        'max_x': 398892.19,
        'min_y': 214783.87,
        'max_y': 726783.87,
        'n_tiles_side': 256
    },
    'split_and_redistribute': {},
    'validate': {}
}
pipeline.config(input_dict)
pipeline.run()

record_file_path = "/tmp/{}_retile_record.js".format(os.path.basename(input_file))

process_tiles_data = []
with open(record_file_path, "r") as record_file:
    records = json.load(record_file)["redistributed_to"]
    for folder_name in records:
        folder_path = "/tmp/{}/".format(folder_name)
        tile_path = folder_path + os.listdir(folder_path)[0]

        ply_path = "/tmp/{}.ply".format(folder_name)

        tile_coords = folder_name.split("_")

        log_path = "/tmp/process_{}_{}.json".format(tile_coords[1], tile_coords[2])
        
        process_tiles_data.append({
            "tile_path": tile_path,
            "ply_path": ply_path,
            "log_path": log_path,
            "x": int(tile_coords[1]),
            "y": int(tile_coords[2]),
        })

        log_files.append(log_path)

print(json.dumps(process_tiles_data))

# Finished retiling
log_retile = log_now()

print("Uploading {} retiled tiles".format(len(process_tiles_data)))
from client import Client
interface = Client()

for retiled_tile in process_tiles_data:
    success = interface.upload(retiled_tile["tile_path"])
    if not success:
        raise Exception("Could not upload file {}".format(retiled_tile["tile_path"]))
    print("Uploaded tile {}".format(retiled_tile["tile_path"]))

# Finished uploading
log_upload = log_now()

with open("/tmp/retile.json", "w") as file_object:
    json_data = json.dumps({
        "start": log_start,
        "download": log_download,
        "retile": log_retile,
        "upload": log_upload,
    })
    file_object.write(json_data)

log_files = ["/tmp/retile.json"]
for process 

with open("/tmp/logs.json", "w") as file_object:
    json_data = json.dumps(log_files)
    file_object.write(json_data)