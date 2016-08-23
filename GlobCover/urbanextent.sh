SOURCEEPSG="EPSG:5070"
DESTEPSG="EPSG:3857"

###################################################
#### This doesn't create a nice contiguous urban cluster, so it may not work for what we need
####################################################

SRCPATH=RawData/GLOBCOVER_L4_200901_200912_V2.3.tif


mkdir scratch
mkdir data

gdal_calc.py -A $SRCPATH \
--outfile=data/globcover_reclassed.tif --calc="0*(A<>190)" --calc="1*(A==190)" --NoDataValue=0 --overwrite

gdal_polygonize.py data/globcover_reclassed.tif  \
-f "ESRI Shapefile" data/globcover_reclassed.shp  \
Globcover_Urban

/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
  -progress \
  -f "PostgreSQL" \
  PG:"host=localhost port=5432 dbname=urbis user=postgres password=postgres" \
  -nln globcoverurbanextent \
  -lco SCHEMA=urbanclusters \
  -where "DN=1" \
  -s_srs EPSG:4326 -t_srs EPSG:3857 \
  -lco OVERWRITE=NO \
  data/globcover_reclassed.shp


psql -d urbis -U postgres -c "CREATE MATERIALIZED VIEW urbanclusters.globcover_urbannamed AS   \
    WITH places as (SELECT neurban.ogc_fid AS id,  \
        (array_agg(tplace.name ORDER BY (st_area(tplace.wkb_geometry)) DESC))[1] AS placename, \
        (array_agg(tplace.ogc_fid ORDER BY (st_area(tplace.wkb_geometry)) DESC))[1] AS placeid, \
        neurban.wkb_geometry AS geom \
       FROM urbanclusters.globcoverurbanextent neurban, \
        urbanclusters.tigerlineplaces tplace \
      WHERE st_intersects(neurban.wkb_geometry, tplace.wkb_geometry) \
      GROUP BY neurban.ogc_fid)\
    SELECT MAX(id) as id, placeid,placename, ST_Union(geom) as geom FROM places\
    GROUP BY placeid, placename \
WITH DATA; \
ALTER TABLE urbanclusters.globcover_urbannamed \
  OWNER TO urbis;"


psql -d urbis -U postgres  -c "CREATE INDEX globcover_urbannamed_geom_idx \
  ON urbanclusters.globcover_urbannamed \
  USING gist \
  (geom);"


    
#nlcd_2006_impervious_2011_edition_2014_10_10