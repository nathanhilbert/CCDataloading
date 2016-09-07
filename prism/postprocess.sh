BASEPATH=/Volumes/UrbisBackup/Workspace/Urbis/DataLoading/prism


# mkdir $BASEPATH/scratch


for f in $BASEPATH/scratch/*.zip
do


    unzip -d $BASEPATH/scratch2 -n $f



  echo "Processing $f file..."
  # take action on each file. $f store current file name
done

mkdir $BASEPATH/data

for z in $BASEPATH/scratch/*.bil 
do
    filebasename=$(basename "$z" ".bil")

    gdalwarp -s_srs "EPSG:4269" -t_srs "EPSG:3857"  \
    -multi -of vrt \
    $z $BASEPATH/scratch2/$filebasename.vrt

    # mkdir data/proj

    # # mkdir $BASEPATH/population$YEAR

    gdal_translate -co compress=LZW $BASEPATH/scratch2/$filebasename.vrt $BASEPATH/data/$filebasename.tif


done

###############################################################
#######THEN RAN on DATA
# gdalbuildvrt ../fulldem.vrt *.tif
# gdal_translate -co compress=LZW ../fulldem.vrt ../fulldem.tif

