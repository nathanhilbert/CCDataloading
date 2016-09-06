Data Usage
--------------------

Vector Data is stored in postgresql:
 - server: ontoserv
 - port: 5434
 - user: urbis

Most raster Data is stored in two formats on //ontodar/urbis/rasterstorage :
 - Tiled used by [pyspatial](https://github.com/granularag/pyspatial).  Used to optimize searches for single urban units.
 - Full raster for QGIS and ArcGIS

Daymet timeseries also stored in //ontodar/urbis/rasterstorage :
 - Full raster for day using a year-day format





Notes
----------------------

Run the shell or python script in each folder then run the cataloger to tile big sets


python ~/Workspace/Urbis/DataLoading/scripts/cataloger/cataloger.py --dest ./nlcd_impervious_2001.json --tiles=./2001 --index=./nlcd_impervious_2001_index.json nlcd_impervious_2001.tif 


Push data to ontoserv
------------------------
psql -U urbis -d urbisdata01 -h ontoserv -p 5434 -f urbanclusters2.sql 
Then refresh all materialized views.