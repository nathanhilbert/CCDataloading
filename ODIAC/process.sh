BASEPATH=/Users/nlh/Workspace/Urbis/DataLoading/ODIAC

mkdir data

# f=$BASEPATH/n08e151.zip
# unzip -d $BASEPATH/scratch -n $f

# FILES=/path/to/*
for f in RawData/*.tif.gz
do

    mkdir scratch


    filebasename=$(basename "$f" ".tif.gz")
    # echo "$filebasename"

    gunzip -c $f > scratch/${filebasename}.tif

    gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:3857"  \
    -multi -of vrt \
    scratch/${filebasename}.tif scratch/${filebasename}.vrt

    # mkdir data/proj

    # # mkdir $BASEPATH/population$YEAR

    gdal_translate -co compress=LZW scratch/${filebasename}.vrt data/${filebasename}.tif


  echo "Processing $f file..."
  rm -rf scratch
  # take action on each file. $f store current file name
done

# mkdir $BASEPATH/data

# for z in $BASEPATH/scratch/*.img 
# do
#     filebasename=$(basename "$z" ".img")

#     gdalwarp -s_srs "EPSG:4269" -t_srs "EPSG:3857"  \
#     -multi -of vrt \
#     $z $BASEPATH/scratch/$filebasename.vrt

#     # mkdir data/proj

#     # # mkdir $BASEPATH/population$YEAR

#     gdal_translate -co compress=LZW $BASEPATH/scratch/$filebasename.vrt $BASEPATH/data/$filebasename.tif


# done

###############################################################
#######THEN RAN on DATA
# gdalbuildvrt ../fulldem.vrt *.tif
# dal_translate -co compress=LZW ../fulldem.vrt ../fulldem.tif

