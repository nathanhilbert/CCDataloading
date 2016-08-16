Tests for Raster Data Storage in DB
===================

Using landscan data

Options
-------------

**Postgres**
 ~~1. Store Tiled rasters in folder location and register via PG - population.landscan~~
 ~~- Add the benefit of allowing other systems to access the tiles~~
 ~~- Can quickly do query on PG to find the tile file names and use them in external program~~
 ~~- Hard to manage the millions of tiles created with 256x256 layout scheme~~

 2. Store full raster in file system and register with tiles in PG - population.landscantiled
   - Again, benefit of other programs accessing the file directly
   - Might slow down query the same as loading the full raster in a row.

 3. Store tiled rasters in the database - population.landscanloadedtile
   - bloated databsae table hard to manage
   - Large amounts of time to make so many transactions

**File System Access**
- Can't take advantage of the related nature of the database system

 4. Store in file system with warped source and process with pyspatial

**Geotrellis and Accumulo**
 5. Store arrays in acculumo registered with hadoop with geoserver display?
   - Difficult to ETL
   - Each analytic would have to be custom programmed, but may still be able to take advantage of spatial joins
   - Using geotrellis could help with some of the geo functions


Tests
--------------------
 - QGIS retrieval and display
    1-3. All data displayed at full extent was too slow to be functional.  #2 has the benefit of allowing the user to connect directly to the source or registering that source in a WMS like Geoserver as well.
    4. Regular speed for qgis rendering with no speed ups or slowdowns.


 - Summation query of statistics for all urban clusters in US
    1018 cities for landscan
    1.  >20 minutes
    2.  >20 minutes
    3.  >20 minutes
    4. 16.6912670135 seconds

 - Time series 
    Random polygon in midwest for 20 days in 1980
    2. Errored Query Run. Not expecting better than 2.5 seconds
    3. 5 minutes 31 seconds
    4. 2.51124811172 seconds 


 - Single stats query of one urban cluster in US
    1. 17.5242609978 seconds
    2. 17.1873991489 seconds
    3. 24.6439399719 seconds
    4. 14.7944848537 seconds


Conclusions
___________________________

 - Raster storage in Postgis are not adequate for our use of fetching all or even 50 cities.
 - This was actually the motivation of building the pyspatial package which provides most of the 
    functionality of postgis in python format.  
 - Storage of projected and compressed rasters as geotiffs on our file systems with pyspatial and geometries being pulled in from 
   Postgis seems to be the best solution for now.  
