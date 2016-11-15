
from io import BytesIO
import os
import sys
import requests
# from shapely.geometry import shape
import os
from subprocess import Popen, PIPE
from multiprocessing import Pool, TimeoutError



try:
  os.mkdir("data")
except:
  pass

try:
  os.mkdir("scratch")
except:
  pass


BASE = "/Volumes/lidar/NGA"


def multiprocessor(fullfilepath):

    from osgeo import ogr, osr
    driver = ogr.GetDriverByName('ESRI Shapefile')

    try:
        ds = driver.Open(fullfilepath)
        if not ds:
            print "\tcould not find!!!!!", fullfilepath
            return False
        layer = ds.GetLayer()
        spatialRef = layer.GetSpatialRef()
        proj4str = str(spatialRef.ExportToProj4())
        args = """/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
          -nlt PROMOTE_TO_MULTI \
          -gt 1000 \
          -s_srs "{0}" -t_srs EPSG:3857 \
           -f "PostgreSQL" \
          PG:"host=ontoserv port=5434 dbname=urbisdata01 user=urbis password=urbis" \
           -append "{1}" -nln buildings3d"""\
          .format(proj4str, fullfilepath)

        pipe = Popen(args, stdout=PIPE, shell=True)
        text = pipe.communicate()[0]
    except Exception,e:
        print "ERROR: ", fullfilepath
        return False

    return True

pool = Pool(processes=6) 
jobs = []
for root, subdirs, files in os.walk(BASE):
    for f in files:
        if f.endswith('.shp') and f.lower().find('3d') != -1:
            fullfilepath = os.path.join(root, f)
            jobs.append(pool.apply_async(multiprocessor, (fullfilepath,)))

totaljobs = len(jobs)
counter = 0
for job in jobs:
    counter +=1
    print counter, "/", totaljobs
    result = job.get()

pool.close()






