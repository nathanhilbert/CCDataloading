#!/bin/bash
mkdir data
mkdir scratch

NODATA=255
FORMAT=Int8


gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:3857" -srcnodata $NODATA \
-dstnodata $NODATA -multi -of vrt \
RawData/consensus_full_class_9.tif scratch/urbanextent.vrt

gdal_translate -co compress=LZW scratch/urbanextent.vrt scratch/urbanextent.tif

gdal_calc.py -A scratch/urbanextent.tif \
--outfile=scratch/urbanextent_reclass.tif --calc="0*(A<1)" --calc="1*(A>0)" --NoDataValue=$NODATA --overwrite


gdal_polygonize.py scratch/urbanextent_reclass.tif \
-f "ESRI Shapefile" scratch/urbanextent.shp \
EarthEnv

/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
  -progress \
  -f "PostgreSQL" \
  PG:"host=localhost port=5432 dbname=urbis user=postgres password=postgres" \
  -nln earthenvurbanextent \
  -lco SCHEMA=urbanclusters \
  -where "DN=1" \
  -s_srs EPSG:3857 -t_srs EPSG:3857 \
  -lco OVERWRITE=NO \
  scratch/urbanextent.shp


psql -d urbis -U postgres -c "CREATE MATERIALIZED VIEW urbanclusters.earthenv_urbannamed AS   \
    WITH places as (SELECT neurban.ogc_fid AS id,  \
        (array_agg(tplace.name ORDER BY (st_area(tplace.wkb_geometry)) DESC))[1] AS placename, \
        (array_agg(tplace.ogc_fid ORDER BY (st_area(tplace.wkb_geometry)) DESC))[1] AS placeid, \
        neurban.wkb_geometry AS geom \
       FROM urbanclusters.earthenvurbanextent neurban, \
        urbanclusters.tigerlineplaces tplace \
      WHERE st_intersects(neurban.wkb_geometry, tplace.wkb_geometry) \
      GROUP BY neurban.ogc_fid)\
    SELECT MAX(id) as id, placeid,placename, ST_Union(geom) as geom FROM places\
    GROUP BY placeid, placename \
WITH DATA; \
ALTER TABLE urbanclusters.earthenv_urbannamed \
  OWNER TO urbis;"


psql -d urbis -U postgres  -c "CREATE INDEX earthenv_urbannamed_geom_idx \
  ON urbanclusters.earthenv_urbannamed \
  USING gist \
  (geom);"