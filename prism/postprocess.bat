BASEPATH=C:\Users\nlh\Workspace\Urbis\pgDataLoading\prism

mkdir $BASEPATH\scratch

FORFILES /M *.zip /c "cmd /C unzip -d ..\scratch -n @path"

FORFILES /M *.bil /c "cmd /C gdalwarp -s_srs EPSG:4269 -t_srs EPSG:3857 -multi -of vrt @path @fname.vrt"


FORFILES /M *.vrt /c "cmd /C gdal_translate -co compress=LZW @path ..\data\(@fname).tif"


###############################################################
#######THEN RAN on DATA
# gdalbuildvrt ../fulldem.vrt *.tif
# dal_translate -co compress=LZW ../fulldem.vrt ../fulldem.tif

