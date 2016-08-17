#!/bin/bash
mkdir data
mkdir scratch
mkdir scratch/urbanextent

NODATA=-9999
FORMAT=Int32

unzip -n -d scratch/urbanextent RawData/gl_grumpv1_urextent_ascii_30.zip

gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:3857" -srcnodata $NODATA \
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
  -where "DN=2" \
  -s_srs EPSG:3857 -t_srs EPSG:3857 \
  -lco OVERWRITE=NO \
  scratch/urbanextent/glurextents.shp 


psql -d urbis -U postgres -c "CREATE MATERIALIZED VIEW urbanclusters.grump_urbannamed AS   \
    WITH places as (SELECT neurban.ogc_fid AS id,  \
        (array_agg(tplace.name ORDER BY (st_area(tplace.wkb_geometry)) DESC))[1] AS placename, \
        (array_agg(tplace.ogc_fid ORDER BY (st_area(tplace.wkb_geometry)) DESC))[1] AS placeid, \
        neurban.wkb_geometry AS geom \
       FROM urbanclusters.grumpurbanextents neurban, \
        urbanclusters.tigerlineplaces tplace \
      WHERE st_intersects(neurban.wkb_geometry, tplace.wkb_geometry) \
      GROUP BY neurban.ogc_fid)\
    SELECT MAX(id) as id, placeid,placename, ST_Union(geom) as geom FROM places\
    GROUP BY placeid, placename \
WITH DATA; \
ALTER TABLE urbanclusters.grump_urbannamed \
  OWNER TO urbis;"


psql -d urbis -U postgres  -c "CREATE INDEX grump_urbannaed_geom_idx \
  ON urbanclusters.grump_urbannamed \
  USING gist \
  (geom);"