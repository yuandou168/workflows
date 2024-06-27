from laserfarm import GeotiffWriter
from log_util import log_now

log_start = log_now()

print("Downloading ply files")
# from client import Client
# interface = Client()


pipeline = GeotiffWriter(input_dir="/tasks/", bands='point_density')
input_dict = {
    'parse_point_cloud': {},
    'data_split': {'xSub': 1, 'ySub': 1},
    'create_subregion_geotiffs': {'output_handle': 'geotiff'}
}
pipeline.config(input_dict)
pipeline.run()

log_end = log_now()
with open("/tmp/rasterize.json", "w") as file_object:
    json_data = json.dumps({
        "start": log_start,
        "end": log_end
    })
    file_object.write(json_data)