#!/bin/bash
mkdir data
mkdir scratch

BASEPATH=/data/rasterstorage/grump

mkdir $BASEPATH

NODATA=-407649103380480



for YEAR in 2000 2005 2010 2015 2020
do 
    unzip -d scratch -n RawData/gpw-v4-population-count-$YEAR.zip

    gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:3857" -srcnodata $NODATA \
    -dstnodata $NODATA -multi -of vrt \
    scratch/gpw-v4-population-count_$YEAR.tif data/gpw-v4-population-count_$YEAR.vrt

    # mkdir $BASEPATH/population$YEAR

    gdal_translate -co compress=LZW data/gpw-v4-population-count_$YEAR.vrt $BASEPATH/population${YEAR}.tif

    #still need to add to the table

    # raster2pgsql -s 3857 -R -a -F -b 1  -t auto -N $NODATA -f raster $BASEPATH/population${YEAR}.tif population.grumppopulation|psql -U postgres -d urbis
    # psql -d urbis -U postgres -c "UPDATE population.grumppopulation SET year=$YEAR WHERE filename LIKE 'gpw-v4-population-count_$YEAR%'"

done