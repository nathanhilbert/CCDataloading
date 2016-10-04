SOURCEEPSG="EPSG:5070"
DESTEPSG="EPSG:3857"

mkdir data
mkdir scratch

for f in RawData/*.tif
do
    

    # ZIPFILE=nlcd_${YEAR}_landcover_2011_edition_2014_10_10.zip

    # echo $ZIPFILE

    # unzip -o -d scratch RawData/$ZIPFILE

    filebasename=$(basename "$f" ".tif")

    gdalwarp -t_srs "EPSG:3857" \
    -multi -of vrt \
    $f scratch/${filebasename}.vrt


    gdal_translate -co compress=LZW scratch/${filebasename}.vrt \
    data/${filebasename}.tif


    # python ~/Workspace/Urbis/DataLoading/scripts/cataloger/cataloger.py \
    # --dest $BASEPATH/nlcd_landcover_${YEAR}.json --tiles=$BASEPATH/${YEAR} --index=$BASEPATH/nlcd_landcover_${YEAR}_index.json \
    # $BASEPATH/nlcd_landcover_${YEAR}.tif


    # rm -rf scratch
done
    
#nlcd_2006_landcover_2011_edition_2014_10_10