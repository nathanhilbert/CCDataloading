
# coding: utf-8

# Grab the tigerplace data from the ftp and load it into postgis
# ---------------


# In[15]:

from ftplib import FTP
from io import BytesIO
import os
import sys
import fiona
import requests
# from shapely.geometry import shape
import os
import zipfile
from subprocess import Popen, PIPE
import requests
from bs4 import BeautifulSoup

def download_file(url, dest):
    if os.path.exists(dest):
        print "skip", dest
        return dest
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return dest


try:
  os.mkdir("data")
except:
  pass

try:
  os.mkdir("scratch")
except:
  pass

BASE = "http://www2.census.gov/geo/tiger/TIGER2010/ROADS/"
if not os.path.exists('data/tigerlineroads.shp'):
    res = requests.get(BASE)
    soup = BeautifulSoup(res.text, 'html.parser')
    tigerlinedata = {}
    for a in soup.find_all('a'):
      if a.text.lower().find("tl_2010_") != -1:
        download_file(BASE + a.text, 'scratch/' + a.text)
        tigerlinedata[a.text] = 'scratch/' + a.text




    # In[23]:

    
    ZIPOUTPUT = 'data/tigerlinedata'

    # # print(zipfile_ob.namelist())
    # for zipped in tigerlinedata.values():
    #     zipfile_ob = zipfile.ZipFile(zipped)
    #     zipfile_ob.extractall(path='data/tigerlinedata/')


    # In[29]:


    features = []
    first = True
    for file in os.listdir(ZIPOUTPUT):
        if file.endswith(".shp"):
          print "doing ", file
          # print "doing this now", os.path.join(ZIPOUTPUT, file)
          # if first:
          #     args = """ogr2ogr -f 'ESRI Shapefile' data/tigerlineroads.shp {0}"""\
          #     .format(os.path.join(ZIPOUTPUT, file))
          #     first = False
          # else:
          args = """/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
            -nlt PROMOTE_TO_MULTI \
            -s_srs EPSG:4269 -t_srs EPSG:3857 \
             -f "PostgreSQL" \
            PG:"host=ontoserv port=5434 dbname=urbisdata01 user=urbis password=urbis" \
             -update -append {0} -nln tigerlineroads \
          -lco SCHEMA=public """\
            .format(os.path.join(ZIPOUTPUT, file))
          
          pipe = Popen(args, stdout=PIPE, shell=True)
          text = pipe.communicate()[0]



    #         with fiona.open(os.path.join(ZIPOUTPUT, file)) as f:
    #             features += [feat for feat in f]
    # print(len(features))
    # polygons =[shape(feature['geometry') for feature in fiona.open("polygons.shp")]
    # from shapely.ops import cascaded_union, unary_union
    # union_poly = cascaded_union(polygons) # or unary_union(polygons)


    # In[31]:



    # In[36]:

    # Define a polygon feature geometry with one attribute
    # OrderedDict([('STATEFP', '01'), ('PLACEFP', '25840'), ('PLACENS', '02403599'), ('GEOID', '0125840'), 
    #              ('NAME', 'Fayette'), ('NAMELSAD', 'Fayette city'), ('LSAD', '25'), ('CLASSFP', 'C1'), 
    #              ('PCICBSA', 'N'), ('PCINECTA', 'N'), ('MTFCC', 'G4110'), ('FUNCSTAT', 'A'), ('ALAND', 22143481), 
    #              ('AWATER', 212108), ('INTPTLAT', '+33.6942153'), ('INTPTLON', '-087.8311690')]
                
    # schema = {'geometry': 'Polygon',
    #     'properties': {'STATEFP': 'str',
    #                   'COUNTYFP': 'str',
    #                   'LINEARID': 'str',
    #                   'FULLNAME': 'str',
    #                   'RTTYP': 'str',
    #                   'MTFCC': 'str'}
    # }

    # # Write a new Shapefile
    # with fiona.open('data/tigerlineroads.shp', 'w', 'ESRI Shapefile', schema) as c:
    #     ## If there are multiple geometries, put the "for" loop here
    #     for f in features:
    #         c.write(f)


# args = """ogr2ogr -f "ESRI Shapefile" data/tigerlinedata3857.shp data/tigerlineroads.shp  -s_srs EPSG:4326 -t_srs \
# EPSG:3857"""
# pipe = Popen(args, stdout=PIPE, shell=True)
# text = pipe.communicate()[0]

# ogr2ogr -update -append -f "PostGreSQL" 
# PG:"host=myserver user=myusername dbname=mydbname password=mypassword" TGR25025.RT1 layer CompleteChain -nln masuf -a_srs "EPSG:4269"


# args = """/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
#   -progress -nlt PROMOTE_TO_MULTI \
#   -f "PostgreSQL" \
#   PG:"host=ontoserv port=5434 dbname=urbisdata01 user=urbis password=urbis" \
#   -nln tigerlineroads \
#   -lco SCHEMA=public \
#   -s_srs EPSG:4269 -t_srs EPSG:3857 \
#   -lco OVERWRITE=YES \
#   data/tigerlinedata3857.shp """

# pipe = Popen(args, stdout=PIPE, shell=True)
# text = pipe.communicate()[0]


# In[ ]:




# In[73]:

# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()



# # In[74]:

# session.rollback()


# # In[75]:

# from shapely.geometry import MultiPolygon
# for feat in features:
#     props = {k.lower():v for k,v in feat['properties'].items()}
#     geometry = shape(feat['geometry'])
#     if geometry.geom_type == 'Polygon':
#         geometry = MultiPolygon([geometry])
#     featobj = TigerLinePlaces(geom=geometry.wkt, **props)
        
        
    

#     session.add(featobj)
#     session.commit()

# lake = Lake(name='Majeur', geom='POLYGON((0 0,1 0,1 1,0 1,0 0))')

# print(shape(features[0]['geometry']))
# for fid, feat in shapefile.items():
#         shapely_geom = shape(feat['geometry'])
#         ga2_geom = WKTElement(shapely_geom.wkt, epsg)


# Method using psycopg2
# 
# ```
# import psycopg2
# import postgis
# db = psycopg2.connect(dbname="urbis", user="postgres", password="postgres", host="localhost")
# cursor = db.cursor()
# postgis.register(cursor)
# cursor.execute("""CREATE TABLE IF NOT EXISTS public.tigerlineplaces ("geom" geometry(POLYGON) NOT NULL,
#                                                                   STATEFP CHAR(50),
#                                                                     PLACEFP CHAR(50),
#                                                                     PLACENS CHAR(50),
#                                                                     GEOID CHAR(50),
#                                                                     NAME CHAR(50) NOT NULL,
#                                                                     NAMELSAD CHAR(50),
#                                                                     LSAD CHAR(50),
#                                                                     CLASSFP CHAR(50),
#                                                                     PCICBSA CHAR(50),
#                                                                     PCINECTA CHAR(50),
#                                                                     MTFCC CHAR(50),
#                                                                     FUNCSTAT CHAR(50),
#                                                                     ALAND INT,
#                                                                     AWATER INT,
#                                                                     INTPTLAT CHAR(50),
#                                                                     INTPTLON CHAR(50))""")
# db.commit()
# 
# for f in features:
#     wfeat = [str(f['geometry'])] + [str(x) for x in f['properties'].values()]
#     cursor.execute("""INSERT INTO public.tigerlineplaces (geom,
#                                                     STATEFP,
#                                                     PLACEFP,
#                                                     PLACENS,
#                                                     GEOID,
#                                                     NAME
#                                                     NAMELSAD, 
#                                                     LSAD, 
#                                                     CLASSFP, 
#                                                     PCICBSA, 
#                                                     PCINECTA, 
#                                                     MTFCC, 
#                                                     FUNCSTAT, 
#                                                     ALAND ,
#                                                     AWATER ,
#                                                     INTPTLAT,
#                                                     INTPTLON) VALUES (%s)""", wfeat)
# db.commit()
# 
# ```

# In[ ]:



