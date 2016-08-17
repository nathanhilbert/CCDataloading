

mkdir data

# wget http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_urban_areas.zip -o data/ne_10m_urban_areas.zip

# unzip -f data/ne_10m_urban_areas -n data/ne_10m_urban_areas.zip 

ogr2ogr -f "ESRI Shapefile" data/ne_10m_urban_areas.shp data/ne_10m_urban_areas/ne_10m_urban_areas.shp   -s_srs EPSG:4326 -t_srs \
EPSG:3857


/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
  -progress -nlt PROMOTE_TO_MULTI \
  -f "PostgreSQL" \
  PG:"host=localhost port=5432 dbname=urbis user=postgres password=postgres" \
  -nln ne_10m_urban_areas \
  -lco SCHEMA=urbanclusters \
  -s_srs EPSG:3857 -t_srs EPSG:3857 \
  -lco OVERWRITE=YES \
  data/ne_10m_urban_areas.shp
