import time
import psutil

def log_now():
  log = {}
  
  log["timestamp"] = time.time()
  net = psutil.net_io_counters(pernic=True)
  if "eth0" in net:
      eth_0 = net["eth0"]
      log["bytes_sent"] = eth_0.bytes_sent
      log["bytes_recv"] = eth_0.bytes_recv
  else:
      log["bytes_sent"] = -1
      log["bytes_recv"] = -1

  return log