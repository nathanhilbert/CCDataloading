#!/bin/bash

BASEPATH=/data/landscan


mkdir data
# -te -20037506 678011 -5383202 18592191 ### used for day met data
gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:3857" -srcnodata -2147483647 -dstnodata -2147483647 -multi -of vrt RawData/LandScanGlobal/lspop2015/w001001.adf data/landscan.vrt
# /Users/nlh/Workspace/sharedata/TestDaymet/daymet_small.tif data/daymet_tester.tif

mkdir $BASEPATH

# $ gdalwarp -tap -tr 30 30 -t_srs "etc..." -of vrt input_file.tif output_file.vrt
gdal_translate -co compress=LZW data/landscan.vrt $BASEPATH/landscan.tif

raster2pgsql -s 3857 -R -a -t auto -F -b 1  -N -2147483647 -f raster $BASEPATH/landscan.tif population.landscan|psql -U postgres -d urbis

# raster2pgsql -s 3857 -c -F -b 1  -N -2147483647 -f raster data/landscancomplete/landscan.tif population.landscancomplete|psql -U postgres -d urbis
