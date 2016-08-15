SOURCEEPSG="EPSG:5070"
DESTEPSG="EPSG:3857"

BASEPATH=/data/nlcd/impervious

# -- Table: population.grumppopulation

# -- DROP TABLE population.grumppopulation;

# CREATE TABLE landcover.nlcdimpervious
# (
#   rid serial NOT NULL,
#   raster raster,
#   filename text,
#   year integer,
#   CONSTRAINT nlcdimpervious_pkey PRIMARY KEY (rid)
# )
# WITH (
#   OIDS=FALSE
# );
# ALTER TABLE landcover.nlcdimpervious
#   OWNER TO postgres;


for YEAR in 2001 2006 2011
do
    mkdir scratch
    mkdir data

    # ZIPFILE=nlcd_${YEAR}_impervious_2011_edition_2014_10_10.zip

    # echo $ZIPFILE

    # unzip -o -d scratch RawData/$ZIPFILE

    gdalwarp -s_srs "EPSG:5070" -t_srs "EPSG:3857" \
    -multi -of vrt \
    RawData/nlcd_${YEAR}_impervious_2011_edition_2014_10_10/nlcd_${YEAR}_impervious_2011_edition_2014_10_10.img data/nlcd_impervious_${YEAR}.vrt

    mkdir $BASEPATH/${YEAR} 

    gdal_translate -co compress=LZW data/nlcd_impervious_${YEAR}.vrt \
    $BASEPATH/nlcd_impervious_${YEAR}.tif

    


    raster2pgsql -s 3857 -R -a -F -b 1 -t auto -N -f raster $FILEPATH landcover.nlcdimpervious |psql -U postgres -d urbis
    psql -d urbis -U postgres -c "UPDATE landcover.nlcdimpervious SET year=${YEAR} WHERE filename LIKE 'nlcd_impervious_${YEAR}%'"
    # gdal_retile.py -v -targetDir /data/nlcd/impervious/${YEAR}  -of GTIFF -co compress=LZW -ot UInt16 -s_srs "EPSG:3857" data/nlcd_impervious_${YEAR}.tif

    # for FILEPATH in /data/nlcd/impervious/${YEAR} 
    # do
    #     raster2pgsql -s 3857 -R -a -F -b 1  -N -f raster $FILEPATH landcover.nlcdimpervious |psql -U postgres -d urbis
    #     psql -d urbis -U postgres -c "UPDATE landcover.nlcdimpervious SET year=${YEAR} WHERE filename LIKE 'nlcd_impervious_${YEAR}%'"
    # done


    rm -rf scratch
    rm -rf data 
done
    
#nlcd_2006_impervious_2011_edition_2014_10_10