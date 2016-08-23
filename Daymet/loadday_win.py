import os
import os.path as op
import os.path as op
from subprocess import Popen, PIPE


try:
    import requests
except ImportError,e:
    package_errors.append('requests - ' + str(e))


try:
    import gdal
    import osr
except ImportError,e:
    package_errors.append('gdal - ' + str(e))

try:
    import numpy as np
except ImportError, e:
    package_errors.append('numpy - ' + str(e))

try:
    import netCDF4
except ImportError, e:
    package_errors.append('netCDF4 - ' + str(e))


SRCPATH=r"C:\UHIData\daymetcache"
#DESTPATH=r"C:\sharedata\rasterstorage\daymet\tmin"
DESTPATH=r"F:\rasterstorage\daymet\tmax"

try:
    os.mkdir(DESTPATH)
except:
    pass

NODATA=-9999

SRCPROJ="+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs"
TARGETPROJ="EPSG:3857"

try:
    os.mkdir('data')
except:
    pass

def gdalrun(netcdfpath, DESTPATH, year, day, datatype):
    nc = netCDF4.Dataset(netcdfpath)
    srs = osr.SpatialReference()
    srs.ImportFromProj4("+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs")
    ncv = nc.variables
    nrows,ncols = np.shape(ncv[datatype][0])
    xmin,ymin,xmax,ymax = [-4560750,-3090500 ,3253250,4984500]
    xres = (xmax-xmin)/float(ncols)
    yres = (ymax-ymin)/float(nrows)
    geotransform=(xmin,xres,0,ymax,0, -yres)

    temptif = 'data/{0}-{1}-{2}-customproj.tif'.format(year, day, datatype)
    output_raster = gdal.GetDriverByName('GTiff')\
            .Create(temptif ,ncols, nrows, 1 ,gdal.GDT_Float32 )  # Open the file
    output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
    output_raster.SetProjection( srs.ExportToWkt() ) 
    try:
        output_raster.GetRasterBand(1).WriteArray(ncv[datatype][day])
    except IndexError,e:
        print "Could not find day {0} and year {1} in the raster for {2}".format(day, year, datatype)
        return None
    output_raster.FlushCache()
    output_raster = None

    tempvrt = 'data/{0}-{1}-{2}-customproj.vrt'.format(year, day, datatype)

    args = """gdalwarp -s_srs "+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs" \
    -t_srs "EPSG:3857" \
    -te -20037506 678011 -5383202 18592191 \
    -multi -of vrt \
    -srcnodata -9999 \
    -dstnodata -9999 \
    {0} \
    {1}""".format(temptif, tempvrt)
    pipe = Popen(args, stdout=PIPE, shell=True)
    text = pipe.communicate()[0]


    args = """gdal_translate -b 1 -co compress=LZW {0} \
            {1}/daymet_v3_tmax_{2}_{3}.tif""".format(tempvrt, DESTPATH, year, day)
    pipe = Popen(args, stdout=PIPE, shell=True)
    text = pipe.communicate()[0]  
    os.remove(tempvrt)
    os.remove(temptif) 
    return text   

for year in range(1980, 2016):
    netcdfpath = r"{0}\daymet_v3_tmax_{1}_na.nc4".format(SRCPATH, year)


    for day in range(1,366):
        if op.exists(op.join(DESTPATH, "daymet_v3_tmax_{0}_{1}.tif".format(year, day) )):
            print "skip", "daymet_v3_tmax_{0}_{1}.tif".format(year, day) 
        else:
            gdalrun(netcdfpath, DESTPATH, year, day, 'tmax')      




