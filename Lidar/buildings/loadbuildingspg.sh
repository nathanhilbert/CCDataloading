#/usr/bin/bash
#
# converts NGA LIDAR building footprint shapefiles into PostGIS SQl
#

. settings.sh

mkdir logs4
mkdir logs4_fix

(cd "$srcdir"; find . -name \*3d\*.shp) | while read fname
do
    if [[ "$fname" =~ ^\./(.*)\.shp$ ]]; then
        tbname=ngalidar4.tb$(
                echo "${BASH_REMATCH[1]}" | \
                md5sum | \
                cut -f1 -d' ' \
                )
    else
      echo Failed to parse filename $fname .
      exit
    fi
    logname=logs4/"$tbname".log
    logname_fix=logs4_fix/"$tbname".log

    if [ -s "$logname" ]; then # file not zero size
    echo Processing $fname \($tbname\)... | tee $logname_fix
        # srid=$(perl -ane 'm/SRID=(\d+)/ && print $1' $logname)

    if [ -z "$srid" ]; then
        echo FUP: Unable to parse out SRID from $fname | tee $logname_fix
    else
            (shp2pgsql -d -s 4326:3857 -g geom -I "$srcdir/$fname" $tbname | psql 2>&1 ) | \
               tee $logname_fix
    fi
    else
    echo $fname skipped...
    fi
done
