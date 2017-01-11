

mkdir data

# wget http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_urban_areas.zip -o data/ne_10m_urban_areas.zip

# unzip -f data/ne_10m_urban_areas -n data/ne_10m_urban_areas.zip 

ogr2ogr -f "ESRI Shapefile" data/ne_10m_urban_areas.shp data/ne_10m_urban_areas/ne_10m_urban_areas.shp   -s_srs EPSG:4326 -t_srs \
EPSG:3857

echo "ADD ID FIELD TO OUTPUT SHAPEFILE"


/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
  -progress -nlt PROMOTE_TO_MULTI \
  -f "PostgreSQL" \
  PG:"host=ontoserv port=5432 dbname=urbisdata01 user=urbis password=urbis" \
  -nln ne_10m_urban_areas \
  -lco SCHEMA=urbandefinitions \
  -s_srs EPSG:3857 -t_srs EPSG:3857 \
  -lco OVERWRITE=YES \
  data/ne_10m_urban_areas.shp

psql -d urbisdata01 -h ontoserv -U urbis -c "CREATE MATERIALIZED VIEW urbandefinitions.ne_10m_urbannamed AS   \
  WITH places as (SELECT neurban.id AS id,  \
      (array_agg(tplace.name ORDER BY (st_area(tplace.geom)) DESC))[1] AS placename, \
      (array_agg(tplace.geoid ORDER BY (st_area(tplace.geom)) DESC))[1] AS placeid, \
      neurban.wkb_geometry AS geom \
     FROM urbandefinitions.ne_10m_urban_areas neurban, \
      population.tigerlineplaces tplace \
    WHERE st_intersects(neurban.wkb_geometry, tplace.geom) \
    GROUP BY neurban.ogc_fid)\
  SELECT MAX(id) as id, placeid,placename, ST_Union(geom) as geom FROM places\
  GROUP BY placeid, placename \
WITH DATA; \
ALTER TABLE urbandefinitions.ne_10m_urbannamed \
OWNER TO urbis;"


psql -d urbisdata01 -h ontoserv -U urbis  -c "CREATE INDEX ne_10m_urbannamed_geom_idx \
ON urbandefinitions.ne_10m_urbannamed \
USING gist \
(geom);"