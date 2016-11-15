BASE = "ftp://ftp.eorc.jaxa.jp/pub/ALOS/ext1/AW3D30/v1604/N020W095_N025W090.tar.gz"
SRCPROJ = "EPSG:4326"

from multiprocessing import Pool, TimeoutError

import os
try:
    os.mkdir("RawData")
except:
    pass

import ftplib


def download_file(urlfile, dest):
    import ftplib
    try:
        ftp = ftplib.FTP("ftp.eorc.jaxa.jp")
        ftp.login()
        ftp.sendcmd("TYPE i") 
        ftp.cwd("/pub/ALOS/ext1/AW3D30/v1604/")
        try:
            size = ftp.size(urlfile)   # Get size of file
        except Exception,e:
            # does not exist in the ftp
            print "file does not exist in FTP", e
            ftp.close()
            return False
        try:
            currentfilesize = os.path.getsize('RawData/{0}'.format(urlfile))
        except:
            currentfilesize = None
        if size == currentfilesize and size and currentfilesize:
            ftp.close()
            print "size and currentfile size match and there is a size in both: Skipping"
            return dest

        
        #cehck size of file before opening the file
        with open(dest, 'wb') as fout:
            if currentfilesize:
                ftp.retrbinary("RETR " + urlfile ,fout.write, currentfilesize)
            else:
                ftp.retrbinary("RETR " + urlfile ,fout.write)

        ftp.close()
        return dest
    except Exception,e:
        print "ERROR: ", e
        try:
            ftp.close()
        except:
            pass
        return False

# def download_file(url, dest):
#     import os
#     import requests
#     try:
#         if os.path.exists(dest):
#             print "skip"
#             return dest
#         # NOTE the stream=True parameter
#         r = requests.get(url, stream=True)
#         with open(dest, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=1024): 
#                 if chunk: # filter out keep-alive new chunks
#                     f.write(chunk)
#                     #f.flush() commented by recommendation from J.F.Sebastian
#         return dest
#     except Exception,e:
#         print "ERROR: ", e
#         return None

pool = Pool(processes=6) 

jobs = []
for n in range(20, 50, 5):
    for w in range(65, 125, 5):
        maxn = str(n + 5).zfill(3)
        minn = str(n).zfill(3)
        maxw = str(w + 5).zfill(3)
        minw = str(w).zfill(3)
        filename = "N{0}W{1}_N{2}W{3}.tar.gz".format(minn, maxw, maxn, minw)
        # fullurl = "ftp://ftp.eorc.jaxa.jp/pub/ALOS/ext1/AW3D30/v1604/{0}"\
        #             .format(filename)
        jobs.append(pool.apply_async(download_file, (filename, os.path.join("RawData", filename))))

totaljobs = len(jobs)
counter = 0
for job in jobs:
    counter +=1
    print counter, "/", totaljobs
    result = job.get()

pool.close()
        

