SRCPATH=/media/staging/urbis/nlh/ontodar/DAYMET/RawData
DESTPATH=/media/staging/urbis/data/rasters/daymet/tmin

# GDALPATH=/Library/Frameworks/GDAL.framework/Versions/1.11/Programs

mkdir $DESTPATH

NODATA=-9999

SRCPROJ="+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs"

mkdir data

for year in $(seq 1980 2015)
do
    gdalwarp -s_srs "$SRCPROJ" -t_srs "EPSG:3857" -srcnodata $NODATA \
        -dstnodata $NODATA -multi -of vrt \
        $SRCPATH/daymet_v3_tmin_${year}_na.nc4 data/daymet_v3_tmin_${year}_na.vrt
    for day in $(seq 1 365)
    do
        echo "${year}-${day}"

        if [ -f "$DESTPATH/daymet_v3_tmin_${year}_${day}.tif" ];
        then
           echo "Skip"
        else
            gdal_translate -b $day -co compress=LZW data/daymet_v3_tmin_${year}_na.vrt \
                $DESTPATH/daymet_v3_tmin_${year}_${day}.tif
        fi
    done
done