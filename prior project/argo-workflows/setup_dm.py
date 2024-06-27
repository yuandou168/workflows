import os
import time
from multiprocessing.connection import Listener

listener = Listener(("127.0.0.1", 20000))

while True:
    try:
        setup_dm_client = listener.accept()
        data_mesh = setup_dm_client.recv()

        if data_mesh == "stop":
            break

        delete_ipfs = "kubectl delete -f /tmp/ipfs.yml"
        result = os.system(delete_ipfs)

        delete_webdav = "kubectl delete -f /tmp/webdav.yml"
        result = os.system(delete_webdav)

        time.sleep(60)

        result = None
        if data_mesh == "ipfs":
            apply_ipfs = "kubectl apply -f /tmp/ipfs.yml"
            result = os.system(apply_ipfs)
        elif data_mesh == "webdav":
            apply_webdav = "kubectl apply -f /tmp/webdav.yml"
            result = os.system(apply_webdav)

        time.sleep(120)

        if result != 0:
            setup_dm_client.send(False)

        setup_dm_client.send(True)
        setup_dm_client.close()
    except:
        pass