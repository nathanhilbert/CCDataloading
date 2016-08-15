#!/bin/bash
mkdir data
mkdir scratch

BASEPATH=/data/grump

NODATA=-407649103380480

# -- Table: population.landscan

# -- DROP TABLE population.landscan;

# CREATE TABLE population.landscan
# (
#   rid serial NOT NULL,
#   raster raster,
#   filename text,
#    year integer,
#   CONSTRAINT landscan_pkey PRIMARY KEY (rid)
# )
# WITH (
#   OIDS=FALSE
# );
# ALTER TABLE population.landscan
#   OWNER TO postgres;

for YEAR in 2000 2005 2010 2015 2020
do 
    unzip -d -n scratch RawData/gpw-v4-population-count-$YEAR.zip
    # /Users/nlh/Workspace/sharedata/TestDaymet/daymet_small.tif data/daymet_tester.tif

# for TIFFPATH in scratch/gpw-v4-population-count_*.tif

    gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:3857" -srcnodata $NODATA \
    -dstnodata $NODATA -multi -of vrt \
    scratch/gpw-v4-population-count_$YEAR.tif data/gpw-v4-population-count_$YEAR.vrt

    mkdir $BASEPATH/population$YEAR

    gdal_translate -co compress=LZW data/gpw-v4-population-count_$YEAR.vrt /data/grump/population${YEAR}.tif

    

    # gdal_retile.py -v -targetDir /data/grump/population$YEAR -of GTIFF \
    # -co compress=LZW -ot Float32 -s_srs "EPSG:3857" data/gpw-v4-population-count_$YEAR.tif
    raster2pgsql -s 3857 -R -a -F -b 1  -t auto -N $NODATA -f raster $BASEPATH/population${YEAR}.tif population.grumppopulation|psql -U postgres -d urbis
    psql -d urbis -U postgres -c "UPDATE population.grumppopulation SET year=$YEAR WHERE filename LIKE 'gpw-v4-population-count_$YEAR%'"
    # for FILEPATH in /data/grump/population$YEAR/*
    # do
    #     raster2pgsql -s 3857 -R -a -F -b 1  -N $NODATA -f raster $FILEPATH population.grumppopulation|psql -U postgres -d urbis
    #     psql -d urbis -U postgres -c "UPDATE population.grumppopulation SET year=$YEAR WHERE filename LIKE 'gpw-v4-population-count_$YEAR%'"
    # done
done