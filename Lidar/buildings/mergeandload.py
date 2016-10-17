
from io import BytesIO
import os
import sys
import requests
# from shapely.geometry import shape
import os
from subprocess import Popen, PIPE



try:
  os.mkdir("data")
except:
  pass

try:
  os.mkdir("scratch")
except:
  pass


BASE = "/Volumes/lidar/NGA"


for root, subdirs, files in os.walk(BASE):
    for f in files:
        if f.endswith('.shp') and f.lower().find('3d') != -1:
            fullfilepath = os.path.join(root, f)
            print "doing", fullfilepath
            args = """/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
              -nlt PROMOTE_TO_MULTI \
              -gt 1000 \
              -s_srs EPSG:32618 -t_srs EPSG:3857 \
               -f "PostgreSQL" \
              PG:"host=ontoserv port=5434 dbname=urbisdata01 user=urbis password=urbis" \
               -append "{0}" -nln buildings3d"""\
              .format(fullfilepath)
            
            pipe = Popen(args, stdout=PIPE, shell=True)
            text = pipe.communicate()[0]



