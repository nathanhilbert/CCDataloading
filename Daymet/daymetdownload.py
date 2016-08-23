from __future__ import absolute_import
from sys import modules

import os.path as op
import os
from subprocess import Popen, PIPE

package_errors = []


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





class DaymetLoader(object):

    def __init__(self, srcfolder):
        self.srcfolder = srcfolder

    def fetchDaymet(self, day=1, year=2105, datatype='tmax', target_epsg="EPSG:4326", dest_dir=""):
        """
        fetch the Daymet or look in the cache for the files
        Return an array with year and days
        """
        finaltiff = '{0}-{1}-{2}.tif'.format(year, day, datatype)

        if op.exists(op.join(self.cachedtiffs, finaltiff)):
            print "skipped"
            return op.abspath(op.join(dest_dir, finaltiff))

        xmin,ymin,xmax,ymax = [-4560750,-3090500 ,3253250,4984500]
        srs = osr.SpatialReference()
        srs.ImportFromProj4("+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs")

        basefile = 'daymet_v3_{0}_{1}_na.nc4'.format(datatype, year)
        netcdfpath = op.join(self.srcfolder, basefile)


        nc = netCDF4.Dataset(netcdfpath)
        ncv = nc.variables
        nrows,ncols = np.shape(ncv[datatype][0])
        xres = (xmax-xmin)/float(ncols)
        yres = (ymax-ymin)/float(nrows)
        geotransform=(xmin,xres,0,ymax,0, -yres)

        temptif = '{0}-{1}-{2}-customproj.tif'.format(year, day, datatype)
        output_raster = gdal.GetDriverByName('GTiff')\
                .Create(op.join(self.cachedtiffs, temptif) ,ncols, nrows, 1 ,gdal.GDT_Float32 )  # Open the file
        output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
        output_raster.SetProjection( srs.ExportToWkt() ) 
        try:
            output_raster.GetRasterBand(1).WriteArray(ncv[datatype][day])
        except IndexError,e:
            self.logger.error("Could not find day {0} and year {1} in the raster for {2}".format(day, year, datatype))
            os.remove(op.join(self.cachedtiffs, temptif))
            return None
        output_raster.FlushCache()
        output_raster = None

        abscachedtiffs = op.abspath(self.cachedtiffs)
        fulltemppath = op.join(abscachedtiffs, temptif)
        fullfinalpath = op.join(abscachedtiffs, finaltiff)

        print fullfinalpath

        args = """gdalwarp -s_srs "+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs" \
        -t_srs {0} \
        -te -20037506 678011 -5383202 18592191 \
        -srcnodata -9999 \
        -dstnodata -9999 \
        {1} \
        {2}""".format(target_epsg, fulltemppath, fullfinalpath)
        pipe = Popen(args, stdout=PIPE, shell=True)
        text = pipe.communicate()[0]

        self.logger.info(text)
        try:
            os.remove(fulltemppath)
        except:
            print "Could not remove temp file"
        if not self.cache_dir:
            os.remove(netcdfpath)
        return fullfinalpath


