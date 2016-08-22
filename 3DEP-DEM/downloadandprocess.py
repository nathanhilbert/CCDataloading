BASE = "http://thor-f5.er.usgs.gov/ngtoc/metadata/waf/elevation/1_arc-second/img/"
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

res = requests.get(BASE)

soup = BeautifulSoup(res.text, 'html.parser')

for a in soup.find_all('a'):
    if a.text.endswith(".xml"):
        fullpath = BASE + '/' + a.text
        
        metares = requests.get(fullpath)
        metasoup = BeautifulSoup(metares.text, 'xml')
        for f in metasoup.find_all('networkr'):
            print f.text
            try:
                download_file(f.text, 'RawData/' + f.text.split('/')[-1])
            except Exception,e:
                print str(e)
    