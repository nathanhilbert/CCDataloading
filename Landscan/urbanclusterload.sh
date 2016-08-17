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


# VIEW
# CREATE MATERIALIZED VIEW urbanclusters.landscan_urbannamed AS 
#  WITH places AS (
#          SELECT neurban.ogc_fid AS id,
#             (array_agg(tplace.name ORDER BY (st_area(tplace.wkb_geometry)) DESC))[1] AS placename,
#             (array_agg(tplace.ogc_fid ORDER BY (st_area(tplace.wkb_geometry)) DESC))[1] AS placeid,
#             neurban.wkb_geometry AS geom
#            FROM urbanclusters.landscanurbancluster neurban,
#             urbanclusters.tigerlineplaces tplace
#           WHERE st_intersects(neurban.wkb_geometry, tplace.wkb_geometry)
#           GROUP BY neurban.ogc_fid
#         )
#  SELECT max(places.id) AS id,
#     places.placeid,
#     places.placename,
#     st_union(places.geom) AS geom
#    FROM places
#   GROUP BY places.placeid, places.placename
# WITH DATA;

# ALTER TABLE urbanclusters.landscan_urbannamed
#   OWNER TO urbis;



# CREATE INDEX landscan_urbannaed_geom_idx
#   ON urbanclusters.landscan_urbannamed
#   USING gist
#   (geom);