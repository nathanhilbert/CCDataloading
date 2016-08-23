BASEPATH=/Volumes/UrbisBackup/Workspace/Urbis/DataLoading/3DEP-DEM

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


# gdalwarp -s_srs "EPSG:4269" -t_srs "EPSG:3857"  \
# -multi -of vrt \
# data/USGS_NED_1_n30w084_IMG.img data/USGS_NED_1_n30w084_IMG.vrt

# mkdir data/proj

# # mkdir $BASEPATH/population$YEAR

# gdal_translate -co compress=LZW data/USGS_NED_1_n30w084_IMG.vrt data/proj/USGS_NED_1_n30w084_IMG.tif

# gdalwarp -s_srs "EPSG:4269" -t_srs "EPSG:3857"  \
# -multi -of vrt \
# data/USGS_NED_1_n30w083_IMG.img data/USGS_NED_1_n30w083_IMG.vrt


# # mkdir $BASEPATH/population$YEAR

# gdal_translate -co compress=LZW data/USGS_NED_1_n30w083_IMG.vrt data/proj/USGS_NED_1_n30w083_IMG.tif


