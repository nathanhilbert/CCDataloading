Landscan 2015 Data
--------------------


Data obtained through email (see below)

 - Download the data to RawData in this directory 
 - Run baseraster.sh


```
From: Rose, Amy N. 
I’ve posted the most current version of LandScan Global and LandScan USA to FTP (see below).  LandScan Global is 2015 – just released at the beginning of this month.  LandScan USA is 2012 – we haven’t updated LSUSA in a few years, but are currently working on an update which we expect to be completed by next spring.
 
I have uploaded the following file for you:

Current LandScan Coverage.zip 187.83 MB

You can get it from

<http://home.ornl.gov/filedownload?ftp=i;dir=uP10FIDbPT3x>

After you have downloaded the file, you can use the following link to delete the file, or send the link back to me so I can delete it.

<http://home.ornl.gov/filedelete?ftp=i;dir=uP10FIDbPT3x>

NOTE: If no previous action is taken, this file will automatically be deleted on 16-Aug-2016.


```





Landscan 2015 Urban Clusters
--------------------

** Run urbanclusterprocess.sh **


Custom Dataset developed by taking the USDA definition of Urban Cluster by
using 500 people/mile^2 with at least one mile of 1000 people/mile^2 in the block.


 - Download the landscan data
 - Reclass any cell values under 193 to 0 and 193 and above to 1
 - Filter out the 0 and NODATA values
 - Vectorize the raster

**To Do: Create script using gdal to do the same process.  See GRUMP/urbanextents**