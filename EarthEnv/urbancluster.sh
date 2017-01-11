#!/bin/bash
mkdir data
mkdir scratch

NODATA=255
FORMAT=Int8


# gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:3857" -srcnodata $NODATA \
# -dstnodata $NODATA -multi -of vrt \
# RawData/consensus_full_class_9.tif scratch/urbanextent.vrt

# gdal_translate -co compress=LZW scratch/urbanextent.vrt scratch/urbanextent.tif

# gdal_calc.py -A scratch/urbanextent.tif \
# --outfile=scratch/urbanextent_reclass.tif --calc="0*(A<1)" --calc="1*(A>0)" --NoDataValue=$NODATA --overwrite


# gdal_polygonize.py scratch/urbanextent_reclass.tif \
# -f "ESRI Shapefile" scratch/urbanextent.shp \
# EarthEnv

# echo "ADD ID FIELD TO urbanextent.shp (press enter when complete)..."
# read text

# /Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
#   -progress \
#   -f "PostgreSQL" \
#   PG:"host=ontoserv port=5432 dbname=urbisdata01 user=urbis password=urbis" \
#   -nln earthenvurbanextent \
#   -lco SCHEMA=urbandefinitions \
#   -where "DN=1" \
#   -s_srs EPSG:3857 -t_srs EPSG:3857 \
#   -lco OVERWRITE=NO \
#   scratch/urbanextent.shp


psql -d urbisdata01 -h ontoserv -U urbis -c "CREATE MATERIALIZED VIEW urbandefinitions.earthenv_urbannamed AS   \
    WITH places as (SELECT neurban.ogc_fid AS id,  \
        (array_agg(tplace.name ORDER BY (st_area(tplace.geom)) DESC))[1] AS placename, \
        (array_agg(tplace.geoid ORDER BY (st_area(tplace.geom)) DESC))[1] AS placeid, \
        neurban.wkb_geometry AS geom \
       FROM urbandefinitions.earthenvurbanextent neurban, \
        population.tigerlineplaces tplace \
      WHERE st_intersects(neurban.wkb_geometry, tplace.geom) \
      GROUP BY neurban.ogc_fid)\
    SELECT MAX(id) as id, placeid,placename, ST_Union(geom) as geom FROM places\
    GROUP BY placeid, placename \
WITH DATA; \
ALTER TABLE urbandefinitions.earthenv_urbannamed \
  OWNER TO urbis;"


psql -d urbisdata01 -h ontoserv -U urbis  -c "CREATE INDEX earthenv_urbannamed_geom_idx \
  ON urbandefinitions.earthenv_urbannamed \
  USING gist \
  (geom);"