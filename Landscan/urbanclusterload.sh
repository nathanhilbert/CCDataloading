#!/bin/bash
SOURCEFILE=/Users/nlh/sharedata/landscan/UrbanClusters/finalurbanclusters.shp

mkdir data

# ogr2ogr -progress \
#         -f "ESRI Shapefile" \
#         $SOURCEFILE data/landscanurbanclusters_projected.shp -s_srs EPSG:4326 -t_srs EPSG:3857


/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
  -progress \
  -f "PostgreSQL" \
  PG:"host=localhost port=5432 dbname=urbis user=postgres password=postgres" \
  -nln landscanurbancluster \
  -lco SCHEMA=urbanclusters \
  -s_srs EPSG:4326 -t_srs EPSG:3857 \
  -lco OVERWRITE=NO \
  $SOURCEFILE 

# find $URBIS_DATA/HSIP_GOLD_2015/Data -name \*.gdb -print0 | \
#   time xargs -0 -n1 -t \
#     ogr2ogr \
#       -progress \
#       -f "PostgreSQL" \
#       PG:"host=ontoserv port=5434 dbname=urbisdata01 user=urbis password=urbis" \
#       -lco SCHEMA=hsip2015test \
#       -lco OVERWRITE=YES \
#       -skipfailures \
#   2>&1 | tee import-$(date +%Y-%m-%dT%H:%m).log

