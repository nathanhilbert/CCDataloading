SOURCEEPSG="EPSG:5070"
DESTEPSG="EPSG:3857"

BASEPATH=/data/rasterstorage/nlcd/impervious

mkdir $BASEPATH


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


    gdal_translate -co compress=LZW data/nlcd_impervious_${YEAR}.vrt \
    $BASEPATH/nlcd_impervious_${YEAR}.tif


    rm -rf scratch
    rm -rf data 
done
    
#nlcd_2006_impervious_2011_edition_2014_10_10