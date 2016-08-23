SOURCEEPSG="EPSG:5070"
DESTEPSG="EPSG:3857"

###################################################
#### This doesn't create a nice contiguous urban cluster, so it may not work for what we need
####################################################

SRCPATH=/data/rasterstorage/nlcd/impervious

mkdir $BASEPATH


for YEAR in 2001 2006 2011
do
    mkdir scratch
    mkdir data

    gdal_calc.py -A /data/rasterstorage/nlcd/impervious/nlcd_impervious_${YEAR}.tif \
    --outfile=data/result_${YEAR}.tif --calc="0*(A<21)" --calc="1*(A>20)" --NoDataValue=0 --overwrite

    gdal_polygonize.py data/result_${YEAR}.tif \
    -f "ESRI Shapefile" scratch/result_${YEAR}.shp \
    NLCD_UrbanExtent

    /Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
      -progress \
      -f "PostgreSQL" \
      PG:"host=localhost port=5432 dbname=urbis user=postgres password=postgres" \
      -nln nlcdurbanextent${YEAR} \
      -lco SCHEMA=urbanclusters \
      -where "DN=1" \
      -s_srs EPSG:3857 -t_srs EPSG:3857 \
      -lco OVERWRITE=NO \
      scratch/result_${YEAR}.shp


    psql -d urbis -U postgres -c "CREATE MATERIALIZED VIEW urbanclusters.nlcd_urbannamed AS   \
        WITH places as (SELECT neurban.ogc_fid AS id,  \
            (array_agg(tplace.name ORDER BY (st_area(tplace.wkb_geometry)) DESC))[1] AS placename, \
            (array_agg(tplace.ogc_fid ORDER BY (st_area(tplace.wkb_geometry)) DESC))[1] AS placeid, \
            neurban.wkb_geometry AS geom \
           FROM urbanclusters.nlcdurbanextent${YEAR} neurban, \
            urbanclusters.tigerlineplaces tplace \
          WHERE st_intersects(neurban.wkb_geometry, tplace.wkb_geometry) \
          GROUP BY neurban.ogc_fid)\
        SELECT MAX(id) as id, placeid,placename, ST_Union(geom) as geom FROM places\
        GROUP BY placeid, placename \
    WITH DATA; \
    ALTER TABLE urbanclusters.nlcd_urbannamed \
      OWNER TO urbis;"


    psql -d urbis -U postgres  -c "CREATE INDEX nlcd_urbannamed_geom_idx \
      ON urbanclusters.nlcd_urbannamed \
      USING gist \
      (geom);"

    rm -rf data
    rm -rf scratch
done
    
#nlcd_2006_impervious_2011_edition_2014_10_10