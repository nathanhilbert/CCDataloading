BASE = "ftp://prism.nacse.org/daily/"

SRCPROJ = "EPSG:4269"

import pandas as pd

import ftplib

import os
try:
    os.mkdir("RawData")
except:
    pass

try:
    os.mkdir("scratch")
except:
    pass

import requests
from bs4 import BeautifulSoup
import traceback






def download_file(baseurl, urlpath, urlfile, dest):
    if os.path.exists(dest):
        print "skip"
        return dest
    ftp = ftplib.FTP("prism.nacse.org")
    ftp.login()

    ftp.cwd(urlpath)
    with open(dest, 'wb') as fout:
        ftp.retrbinary("RETR " + urlfile ,fout.write)

    ftp.close()


    # # NOTE the stream=True parameter
    # r = requests.get(url, stream=True)
    # with open(dest, 'wb') as f:
    #     for chunk in r.iter_content(chunk_size=1024): 
    #         if chunk: # filter out keep-alive new chunks
    #             f.write(chunk)
    #             #f.flush() commented by recommendation from J.F.Sebastian
    # return dest



for measure in ('tmax', 'tmin',):
    for year in range(1981, 2017):
        rng = pd.date_range('1/1/{0}'.format(year), periods=366, freq='D')
        for daydate in rng:
            print daydate
            try:
                filename = "PRISM_{0}_stable_4kmD1_{1}{2}{3}_bil.zip".format(measure, daydate.year, 
                        str(daydate.month).zfill(2), 
                        str(daydate.day).zfill(2))
                download_file('ftp://prism.nacse.org',
                            '/daily/{0}/{1}'.format(measure, year),
                            '{0}'.format(filename),
                            'scratch/{0}'.format(filename))
            except Exception,e:
                print e
                # download_file('/daily/{0}/{1}'.format(measure, year),
                #                 filename,
                #                 'scratch/{0}'.format(filename),
                #                 ftp)

                #name = ftp://prism.nacse.org/daily/tmax/1981/PRISM_tmax_stable_4kmD1_19810101_bil.zip






# res = requests.get(BASE)

# soup = BeautifulSoup(res.text, 'html.parser')

# for a in soup.find_all('a'):
#     if a.text.endswith(".xml"):
#         fullpath = BASE + '/' + a.text
        
#         metares = requests.get(fullpath)
#         metasoup = BeautifulSoup(metares.text, 'xml')
#         for f in metasoup.find_all('networkr'):
#             print f.text
#             try:
#                 download_file(f.text, 'RawData/' + f.text.split('/')[-1])
#             except Exception,e:
#                 print str(e)
#     