import os
import shutil
import time

for root, dirs, files in os.walk("/tmp/"):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

time.sleep(5)