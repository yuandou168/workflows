import os
import time
import re
import sys


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


def get_FileSize(file):
    file = str(file)
    fsize = os.path.getsize(file)
    # print(fsize)
    fsize = fsize/float(1000*1000)
    return round(fsize,2)

# def cut_text(text,num):
#     x=int(len(text)/num)
#     textArr = re.findall(r".{"+str(x)+r"}|.+?$", text)
#     return textArr

def splitTXTFile(bigfile, num, ddir):
  filenamelist = []
  with open(bigfile, 'r') as f:
    content = f.readline()

  # record time
  starttime = getnowdatatime()
  startclock = time.time()    
  p = int(len(content)/num)
  for i in range(num):
    chunk = content[i*p:(i+1)*p]
    # print('chunk: {chunk}')  
    filename = getnowdatatime(3) + '_' + 'split' + str(i) + '.txt'
    print(f'filename：{filename}')
    filepath = ddir
    filenamelist.append(filepath+filename)
    f = open(filepath + filename, 'w')
    f.write(chunk)   
    f.close()
          
  print(f'partition big file, single file size:{sys.getsizeof(chunk)/(1000*1000)}MB., no. of files: {len(filenamelist)}\n')
  print(f'DetailInfo:')
  print(f'path: {filepath + filename}')
  print(f'start:{starttime}')
  print(f'end:{getnowdatatime()}')
  print(f'time cost:{(time.time() - startclock):<.3}sec.')
  return filenamelist

if __name__ == '__main__':
    splitTXTFile('./files/20210701211029_10MB.txt', 5, './split/')