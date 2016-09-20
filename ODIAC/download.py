BASE = "http://db.cger.nies.go.jp/dataset/ODIAC/data/odiac2015a/1km/2014/odiac2015a_1km_excl_intl_1401.tif.gz"
# http://db.cger.nies.go.jp/dataset/ODIAC/data/odiac2015a/1km/2000/odiac2015a_1km_excl_intl_0001.tif.gz
SRCPROJ = "EPSG:4269"


import os
try:
    os.mkdir("RawData")
except:
    pass

import requests
from bs4 import BeautifulSoup

def download_file(url, dest):
    if os.path.exists(dest):
        print "skip"
        return dest
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return dest


for year in range(0,15):
    for month in range(1, 13):
        filename = "odiac2015a_1km_excl_intl_{0}{1}.tif.gz".format(str(year).zfill(2), str(month).zfill(2))
        fullurl = "http://db.cger.nies.go.jp/dataset/ODIAC/data/odiac2015a/1km/20{0}/{1}".format(str(year).zfill(2), filename)
        try:
            download_file(fullurl, 'RawData/' + filename)
        except Exception,e:
            print e

