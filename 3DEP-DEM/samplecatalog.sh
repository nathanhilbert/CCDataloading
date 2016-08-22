gdalwarp -s_srs "EPSG:4269" -t_srs "EPSG:3857"  \
-multi -of vrt \
data/USGS_NED_1_n30w084_IMG.img data/USGS_NED_1_n30w084_IMG.vrt

mkdir data/proj

# mkdir $BASEPATH/population$YEAR

gdal_translate -co compress=LZW data/USGS_NED_1_n30w084_IMG.vrt data/proj/USGS_NED_1_n30w084_IMG.tif

gdalwarp -s_srs "EPSG:4269" -t_srs "EPSG:3857"  \
-multi -of vrt \
data/USGS_NED_1_n30w083_IMG.img data/USGS_NED_1_n30w083_IMG.vrt


# mkdir $BASEPATH/population$YEAR

gdal_translate -co compress=LZW data/USGS_NED_1_n30w083_IMG.vrt data/proj/USGS_NED_1_n30w083_IMG.tif


