import os
import time

# timestamp
def getnowdatatime(flag=0):

  now = time.localtime(time.time())
  if flag == 0:
    return time.strftime('%Y-%m-%d %H:%M:%S', now)
  if flag == 1:
    return time.strftime('%Y-%m-%d', now)
  if flag == 2:
    return time.strftime('%H:%M:%S', now)
  if flag == 3:
    return time.strftime('%Y%m%d%H%M%S', now)

# get file size
def get_FileSize(file):
    file = str(file)
    fsize = os.path.getsize(file)
    print(fsize)
    fsize = fsize/float(1000*1000)
    return round(fsize,2)

# merge file from file list
def mergeTXTFile(indir, filelist, outdir):
    filename = getnowdatatime(3) + '_' + 'Merged.txt'
    print(f'Filename: {filename}')
    filepath = outdir
    f = open(filepath + filename, 'w')

    starttime = getnowdatatime()
    startclock = time.time()
    # traversal the filelist and read lines 
    for item in filelist:    
        for txt in open(indir + item, 'r'):    
            f.write(txt)  
    # close file  
    f.close()  
    fileSize = get_FileSize(filepath+filename)
    print(f'merged file size:{fileSize}MB.\n')
    print(f'DetailInfo:')
    print(f'storage path: {filepath + filename}')
    print(f'startime:{starttime}')
    print(f'endtime:{getnowdatatime()}')
    print(f'time consumed:{(time.time() - startclock):<.3}sec.')
    return filepath + filename

# if __name__ == '__main__':
    # filelist = ['./files/20210613150630_60MB.txt', './files/20210613151430_10MB.txt']
    # mergeTXTFile(indir, filelist, outdir)