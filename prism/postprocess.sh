BASEPATH=/Volumes/UrbisBackup/Workspace/Urbis/DataLoading/prism

mkdir $BASEPATH/scratch

# f=$BASEPATH/n08e151.zip
# unzip -d $BASEPATH/scratch -n $f

# FILES=/path/to/*
for f in $BASEPATH/*.zip
do


    unzip -d $BASEPATH/scratch -n $f



  echo "Processing $f file..."
  # take action on each file. $f store current file name
done

mkdir $BASEPATH/data

for z in $BASEPATH/scratch/*.img 
do
    filebasename=$(basename "$z" ".img")

    gdalwarp -s_srs "EPSG:4269" -t_srs "EPSG:3857"  \
    -multi -of vrt \
    $z $BASEPATH/scratch/$filebasename.vrt

    # mkdir data/proj

    # # mkdir $BASEPATH/population$YEAR

    gdal_translate -co compress=LZW $BASEPATH/scratch/$filebasename.vrt $BASEPATH/data/$filebasename.tif


done

###############################################################
#######THEN RAN on DATA
# gdalbuildvrt ../fulldem.vrt *.tif
# dal_translate -co compress=LZW ../fulldem.vrt ../fulldem.tif

