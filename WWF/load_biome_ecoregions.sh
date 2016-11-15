/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
            -nlt PROMOTE_TO_MULTI \
            -s_srs EPSG:4326 -t_srs EPSG:3857 \
             -f "PostgreSQL" \
            PG:"host=ontoserv port=5434 dbname=urbisdata01 user=urbis password=urbis" \
             -update -append RawData/wwf_terr_ecos.shp -nln wwf_terr_ecos \
          -lco SCHEMA=public 