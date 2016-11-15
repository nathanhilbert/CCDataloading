BASEPATH=/Users/nlh/Workspace/Urbis/DataLoading/EORC-ALOS

mkdir $BASEPATH/scratch

# f=$BASEPATH/n08e151.zip
# unzip -d $BASEPATH/scratch -n $f

# FILES=/path/to/*
for f in $BASEPATH/RawData/*.tar.gz
do

    mkdir temp

    FILEBASENAME=$(basename "$f" ".tar.gz")


    tar -zxv -C $BASEPATH/temp -f $f

    cp -f $BASEPATH/temp/$FILEBASENAME/AVERAGE/* $BASEPATH/scratch

    cp -f $BASEPATH/temp/$FILEBASENAME/MEDIAN/* $BASEPATH/scratch



    rm -rf temp

  echo "Processing $f file..."
  # take action on each file. $f store current file name
done

# Then create a tile index to make sure I got everything
# gdaltindex ../totaltile2.shp ./*_MED_DSM.tif

# gdalbuildvrt /Volumes/URBIS/Dataloading/EORC-ALOS/dsm_med.vrt ./*_MED_DSM.tif

# gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:3857" -multi -of vrt $BASEPATH/dsm_med.vrt $BASEPATH/dsm_med_proj.vrt

# gdal_translate -co compress=LZW -co BIGTIFF=YES /Volumes/URBIS/Dataloading/EORC-ALOS/dsm_med_proj.vrt $BASEPATH/data/dsm_med.tif



