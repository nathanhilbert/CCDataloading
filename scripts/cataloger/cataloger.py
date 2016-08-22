"""
Copyright (c) 2016, Granular, Inc. 
All rights reserved.
License: BSD 3-Clause ("BSD New" or "BSD Simplified")
Redistribution and use in source and binary forms, with or without modification, are permitted 
provided that the following conditions are met: 
  * Redistributions of source code must retain the above copyright notice, this list of conditions 
    and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the 
    following disclaimer in the documentation and/or other materials provided with the distribution. 
  * Neither the name of the nor the names of its contributors may be used to endorse or promote products 
    derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS 
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
 AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BE LIABLE FOR ANY DIRECT, 
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



Example Run

python cataloger.py --dest=/path/to/something/filename.json --tiles=/path/to/something/tiled srcfile.tif

"""
import tempfile
import os
import os.path as op
import argparse
import json
from pyspatial.vector import read_layer, read_geojson
from pyspatial.utils import projection_from_string
import gdal


# FROM https://github.com/granularag/pyspatial/blob/master/examples/creating_a_tiled_raster.ipynb
from osgeo import gdal
import subprocess
import os
from itertools import product





def buildTiles(src, tiledest, indextmp= None):
    #Parameters
    #Use the files ending in .img for the CDL
    filename = "/data/rasterstorage/nlcd/impervious/nlcd_impervious_2011.tif"

    tilesize = 5240

    fileDir = src
    tileDir = tiledest
    # indexDir = indextmp
    ds = gdal.Open(filename)
    driver = ds.GetDriver()
    fileType = driver.GetDescription()

    if not os.path.exists(tileDir):
        os.makedirs(tileDir)

    # if not os.path.exists(indexDir):
    #     os.makedirs(indexDir)

    def create_tile(tup, tilesize=5240):
        i, j = tup
        w = min(i+tilesize, width) - i
        h = min(j+tilesize, height) - j
        srcwin = ["-srcwin"]
        window = [i, j, w, h]
        srcwin.extend(map(str, window))
        outfilename = os.path.join(tileDir, "_".join(map(str, [i, j])))
        args = ["gdal_translate","-of", "GTIFF", "-co", "compress=LZW"] + srcwin 
        args += [filename, outfilename+".tif"]
        try:
            subprocess.check_call(args)
        except:
            print " ".join(args)
            raise
        return args[-1]
        
    ds = gdal.Open(filename)
    width = ds.RasterXSize
    height = ds.RasterYSize
    driver = ds.GetDriver()
    fileType = driver.GetDescription()

    if not os.path.exists(tileDir):
        os.makedirs(tileDir)

    #Close the file
    ds = None
    tups = [(i,j) for i in range(0, width, tilesize) for j in range(0, height, tilesize)]
    outfilenames = map(lambda x: create_tile(x, tilesize=tilesize), tups)


    # In[ ]:

    #Create Index File (Optional)
    # index_args = ["gdaltindex", "-f", "GEOJSON", "-t_srs", "EPSG:3857"]
    # index_filename = indextmp
    # input_files = [os.path.join(tileDir, f) for f in os.listdir(tileDir) if f.endswith(".tif")]
    # index_args.append(index_filename)
    # index_args.extend(input_files)

    # if os.path.exists(index_filename):
    #     os.remove(index_filename)

    # #Run the command
    # subprocess.check_output(index_args)

    return True







def createCatalog(src, tile_path, dest, index_path=None, grid=None):

    hDataset = gdal.OpenShared(src)

    # Get projection.
    proj = hDataset.GetProjectionRef()

    # Dump to json
    catalog = {"Path": src,
               "CoordinateSystem": proj,
               "GeoTransform": hDataset.GetGeoTransform()}

    band = hDataset.GetRasterBand(1)
    ctable = band.GetColorTable()

    if ctable is not None:
        colors = [ctable.GetColorEntry(i) for i in range(256)]
        catalog["ColorTable"] = colors

    xsize = hDataset.RasterXSize
    ysize = hDataset.RasterYSize
    catalog["Size"] = (xsize, ysize)

    if tile_path is not None:
        if os.path.exists(tile_path):
            tiles = os.listdir(tile_path)
            if len(tiles) == 0:
                raise ValueError("%s is empty" % tile_path)

            tile = os.path.join(tile_path, tiles[0])
            ds = gdal.OpenShared(tile)
            if ds is None:
                raise ValueError("Unable to open file: %s" % tile)

            xsize = ds.RasterXSize
            ysize = ds.RasterYSize
            if xsize != ysize:
                raise ValueError("tiles must have same X and Y size")

            catalog["GridSize"] = xsize
            catalog["Path"] = tile_path
        else:
            raise ValueError("tiles path does not exist: %s" % tile_path)

    if index_path is not None:
        read = read_geojson if index_path.endswith("json") else read_layer
        index = read(index_path)
        catalog["Index"] = index.transform(projection_from_string()).to_dict()

    if dest is not None:
        with open(dest, "w+b") as outf:
            outf.write(json.dumps(catalog))
    else:
        print json.dumps(catalog)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create json catalog file.')
    parser.add_argument('src', help='The source raster file')

    parser.add_argument('--dest', dest="dest",
                        help='The output path for the json file',
                        default=None)
    parser.add_argument('--tiles', dest='tile_path', default=None,
                        help='Specify path to save tiles')
    parser.add_argument('--index', dest='index_path', default=None)

    args = parser.parse_args()

    if op.exists(args.tile_path) and len(os.listdir(args.tile_path)) < 10:

        result = buildTiles(src=os.path.abspath(args.src), tiledest=os.path.abspath(args.tile_path))
    else:
        result = True

    if result:
        createCatalog(src=os.path.abspath(args.src), tile_path=os.path.abspath(args.tile_path), dest=os.path.abspath(args.dest))

