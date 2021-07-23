# !/user/bin/env python
# -*- coding:utf-8 -*-
 
import os
import time


def getnowdatatime(flag=0):
  '''
  flag = 0  eg:2018-04-11 10:04:55
  flag = 1  eg:2018-04-11
  flag = 2  eg:10:04:55
  flag = 3  eg:20180411100455
  '''
  now = time.localtime(time.time())
  if flag == 0:
    return time.strftime('%Y-%m-%d %H:%M:%S', now)
  if flag == 1:
    return time.strftime('%Y-%m-%d', now)
  if flag == 2:
    return time.strftime('%H:%M:%S', now)
  if flag == 3:
    return time.strftime('%Y%m%d%H%M%S', now)
 
 
# generate a file with predefined size
def generateTXTFile(filepath, fileSize):
  if fileSize >= 200:
    print('creating a file, please waiting... ...')
  filename = getnowdatatime(3) + '_' + str(fileSize) + 'MB.txt'
  print(f'filepath: {filepath}; filename：{filename}')
  f = open(filepath + filename, 'w')
  starttime = getnowdatatime()
  startclock = time.time()

  for i in range(fileSize):
    if i >= 100:
      if i % 100 == 0:
        print(f'generated {i//100 * 100}MB data.')
    for j in range(1000):
      try:
        f.write('01' * 500)
      except KeyboardInterrupt:
        print('\nAbnormal Interruption!:KeyboardInterrupt')
        f.close()
        exit(-1)
  f.close()
  print(f'generated file, size:{fileSize}MB.\n', os.path.getsize(filepath + filename))
  print(f'DetailInfo:')
  print(f'path: {filepath + filename}')
  print(f'start:{starttime}')
  print(f'end:{getnowdatatime()}')
  print(f'time cost:{(time.time() - startclock):<.3}sec.')
  return filepath + filename
 
 
if __name__ == '__main__':
  x = generateTXTFile('./files/', 1)
  print(x)