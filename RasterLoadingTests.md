Tests for Raster Data Storage in DB
-----------------------

Using landscan data

Options

 1. Store Tiled rasters in folder location and register via PG - population.landscan
   - Add the benefit of allowing other systems to access the tiles
   - Can quickly do query on PG to find the tile file names and use them in external program
   - Hard to manage the millions of tiles created with 256x256 layout scheme

 2. Store full raster in file system and register with tiles in PG - population.landscantiled
   - Again, benefit of other programs accessing the file directly
   - Might slow down query the same as loading the full raster in a row.

 3. Store tiled rasters in the database - population.landscanloadedtile
   - bloated databsae table hard to manage
   - Large amounts of time to make so many transactions

**Not tested**

 4. Store and process everything using stored files?
   - Can't take advantage of the related nature of the database system
   - Extra processing and programming time

 5. Store arrays in acculumo registered with hadoop with geoserver display?
   - Difficult to ETL
   - Each analytic would have to be custom programmed, but may still be able to take advantage of spatial joins
   - Using geotrellis could help with some of the geo functions


**Tests**
 - QGIS retrieval and display
    All. All data displayed at full extent was too slow to be functional.  #2 has the benefit of allowing the user to connect directly to the source or registering that source in a WMS like Geoserver as well.
 - Summation query of statistics for all urban clusters in US
 - Single stats query of one urban cluster in US
    1. 17.5242609978 seconds
    2. 17.1873991489 seconds
    3. 24.6439399719 seconds
