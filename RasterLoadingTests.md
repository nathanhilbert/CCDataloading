Tests for Raster Data Storage in DB
-----------------------

Using landscan data

Options

 1. Store full raster in the database as row
   - Slow for iterative calculations e.g. show total popultion of all cities in the US
   - Bloated Database tables make it difficult for backup

 2. Store Tiled rasters in folder location and register via PG
   - Add the benefit of allowing other systems to access the tiles
   - Can quickly do query on PG to find the tile file names and use them in external program
   - Hard to manage the millions of tiles created with 256x256 layout scheme

 3. Store full raster in file system and register with tiles in PG
   - Again, benefit of other programs accessing the file directly
   - Might slow down query the same as loading the full raster in a row.

 4. Store tiled rasters in the database
   - bloated databsae table hard to manage
   - Large amounts of time to make so many transactions


**Tests**


 - Load time
 - QGIS retrieval and display
    2. Very slow display in QGIS using the tiles.  Attempted to use st_Union with view, but could not load the layer
 - Summation query of statistics for all urban clusters in US
 - Single stats query of one urban cluster in US
