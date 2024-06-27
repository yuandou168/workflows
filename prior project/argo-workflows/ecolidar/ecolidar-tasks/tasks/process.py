from laserfarm import DataProcessing
import json
import sys
from log_util import log_now

log_start = log_now()

args = json.loads(sys.argv[1])
tile_path = args["tile_path"]
ply_path = args["ply_path"]
log_path = args["log_path"]
tile_index = (args["x"], args["y"])

print("Downloading tile {}".format(tile_path))
# from client import Client
# interface = Client()
# success = interface.download(tile_path)
# if not success:
#     raise Exception("Could not download tile {}".format(tile_path))

pipeline = DataProcessing(input=tile_path, tile_index=tile_index)
input_dict = {
    'load': {},
    'normalize': {'cell_size': 1},
    'generate_targets': {
        'min_x': -113107.81,
        'max_x': 398892.19,
        'min_y': 214783.87,
        'max_y': 726783.87,
        'n_tiles_side': 256,
        'tile_mesh_size' : 10.,
        'validate' : True,
    },
    'extract_features': {
        'volume_type': 'cell',
        'volume_size': 10.,
        'feature_names': ['point_density']
    },
    'export_targets': {}
}
pipeline.config(input_dict)
pipeline.run()

print("Uploading ply {}".format(ply_path))
# success = interface.upload(ply_path)
# if not success:
#     raise Exception("Could not upload ply file {}".format(ply_path))

log_end = log_now()
with open(log_path, "w") as file_object:
    json_data = json.dumps({
        "start": log_start,
        "end": log_end
    })
    file_object.write(json_data)

print("Uploading log {}".format(log_path))
# success = interface.upload(log_path)
# if not success:
#     raise Exception("Could not upload log file {}".format(log_path))