import sys
from multiprocessing.connection import Client

setup_dm_listener = Client(("127.0.0.1", 20000))

data_mesh = sys.argv[1]
setup_dm_listener.send(data_mesh)

success = setup_dm_listener.recv()
if not success:
    raise Exception("Could not setup data mesh {}".format(data_mesh))

setup_dm_listener.close()