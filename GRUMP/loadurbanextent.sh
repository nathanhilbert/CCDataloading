#!/bin/bash
mkdir data
mkdir scratch
mkdir scratch/urbanextent

NODATA=-9999
FORMAT=Int32

unzip -d scratch/urbanextent RawData/gl_grumpv1_urextent_ascii_30.zip

gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:3857" -srcnodata $NODATA \
-cwhere 
-dstnodata $NODATA -multi -of vrt \
scratch/urbanextent/glurextents.asc scratch/urbanextent/glurextents.vrt

gdal_translate -co compress=LZW scratch/urbanextent/glurextents.vrt scratch/urbanextent/glurextents.tif


gdal_polygonize.py scratch/urbanextent/glurextents.tif \
-f "ESRI Shapefile" scratch/urbanextent/glurextents.shp \
Grump_urbanextentPolygons

/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
  -progress \
  -f "PostgreSQL" \
  PG:"host=localhost port=5432 dbname=urbis user=postgres password=postgres" \
  -nln grumpurbanextents \
  -lco SCHEMA=urbanclusters \
  -s_srs EPSG:3857 -t_srs EPSG:3857 \
  -lco OVERWRITE=NO \
  scratch/urbanextent/glurextents.shp 
