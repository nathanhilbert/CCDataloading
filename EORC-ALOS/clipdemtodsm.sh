# clip dem to the size of the dsm
gdal_translate -of GTiff -ot Float32 -projwin -13914936.3492 6446275.84102 -7235756.1953 2273031.59216 -co COMPRESS=LZW -co PREDICTOR=1 -co BIGTIFF=YES /Volumes/URBIS/rasterstorage/dem/dem.tif ./clippeddem.tif


#subtract the dsm from the dem
gdal_calc.py --calc "A-B" --format GTiff --type Float32 -A /Volumes/URBIS/rasterstorage/eroc-alos/dsm_avg.tif --A_band 1 -B ./clippeddem.tif --B_band 1 --outfile ./tester.tif
