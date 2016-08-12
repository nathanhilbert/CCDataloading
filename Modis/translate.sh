GDALINFO=/Library/Frameworks/GDAL.framework/Programs
THEPATH=/Users/nlh/Downloads

mkdir data

$GDALINFO/gdalinfo $THEPATH/MOD11A1.A2000055.h12v12.006.2015057070628.hdf

# Daytime temperature HDF4_EOS:EOS_GRID:"/Users/nlh/Downloads/MOD11A1.A2000055.h00v09.006.2015057070300.hdf":MODIS_Grid_Daily_1km_LST:LST_Day_1km
# This is night time temperature MODIS_Grid_Daily_1km_LST
# See https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod11a1

$GDALINFO/gdal_translate -a_srs "EPSG:4326"  \
HDF4_EOS:EOS_GRID:"/Users/nlh/Downloads/MOD11A1.A2000055.h12v12.006.2015057070628.hdf":MODIS_Grid_Daily_1km_LST:LST_Night_1km \
data/mod_nighttemp.tif

$GDALINFO/gdal_translate -a_srs "EPSG:4326"  \
HDF4_EOS:EOS_GRID:"/Users/nlh/Downloads/MOD11A1.A2000055.h12v12.006.2015057070628.hdf":MODIS_Grid_Daily_1km_LST:LST_Day_1km \
data/mod_daytemp.tif