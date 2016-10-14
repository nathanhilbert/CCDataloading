#
# settings and checks for making NGA LIDAR database
#

# quit on failure
set -e

#srcdir=/Volumes/LiDAR/NGA
srcdir=/Volumes/lidar/NGA
depdir=.deps
logf=logs/import-$(date +%F-%T).log

db_host=ontoserv
db_name=urbis
db_user=urbis
db_schema=lidar
db_table="$db_schema.bfootprints"
srs_id=3857

#shp2pgsql="/opt/local/lib/postgresql84/bin/shp2pgsql -W latin1 -s $srs_id"
#psql="psql84 -h $db_host -d $db_name -U $db_user"

shp2pgsql="shp2pgsql -W latin1 -s $srs_id -g geom -I "
psql="psql -h $db_host -d $db_name -U $db_user"

if [ ! -d "$srcdir" ]; then
    echo LIDAR direcotyr $srcdir does not seem to be mounted
    exit
fi

#if [ ! -x "$shp2pgsql" ]; then
#    echo Unable to find $shp2pgsql
#    exit
#fi

