
# coding: utf-8

# Grab the tigerplace data from the ftp and load it into postgis
# ---------------


# In[15]:

from ftplib import FTP
from io import BytesIO
import os
import sys
import fiona
# from shapely.geometry import shape
import os
import zipfile
from subprocess import Popen, PIPE


try:
  os.mkdir("data")
except:
  pass


if not os.path.exists('data/tigerlineplaces.shp'):



    ftp = FTP('ftp2.census.gov') #/geo/tiger/TIGER2015/PLACE/
    ftp.login() 
    ftp.cwd('geo/tiger/TIGER2015/PLACE/')

    filenames = ftp.nlst() # get filenames within the directory

    tigerlinedata = {}

    for filename in filenames:
        print("Downloading %s"%filename)
        file = BytesIO()
        ftp.retrbinary('RETR '+ filename, file.write)
        tigerlinedata[filename] = file

    ftp.quit() # This is the “polite” way to close a connection



    # In[23]:

    
    ZIPOUTPUT = 'data/tigerlinedata'

    # print(zipfile_ob.namelist())
    for zipped in tigerlinedata.values():
        zipfile_ob = zipfile.ZipFile(zipped)
        zipfile_ob.extractall(path='data/tigerlinedata/')


    # In[29]:


    features = []
    for file in os.listdir(ZIPOUTPUT):
        if file.endswith(".shp"):
            with fiona.open(os.path.join(ZIPOUTPUT, file)) as f:
                features += [feat for feat in f]
    print(len(features))
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
                
    schema = {'geometry': 'Polygon',
        'properties': {'STATEFP': 'str',
                      'PLACEFP': 'str',
                      'PLACENS': 'str',
                      'GEOID': 'str',
                      'NAME': 'str',
                      'NAMELSAD': 'str',
                      'LSAD': 'str',
                      'CLASSFP': 'str',
                      'PCICBSA': 'str',
                      'PCINECTA': 'str',
                      'MTFCC': 'str',
                      'FUNCSTAT': 'str',
                      'ALAND': 'int',
                      'AWATER': 'int',
                      'INTPTLAT': 'str',
                      'INTPTLON': 'str'}
    }

    # Write a new Shapefile
    with fiona.open('data/tigerlineplaces.shp', 'w', 'ESRI Shapefile', schema) as c:
        ## If there are multiple geometries, put the "for" loop here
        for f in features:
            c.write(f)




args = """ogr2ogr -f "ESRI Shapefile" data/tigerlineplaces3857.shp data/tigerlineplaces.shp  -s_srs EPSG:4326 -t_srs \
EPSG:3857"""
pipe = Popen(args, stdout=PIPE, shell=True)
text = pipe.communicate()[0]


args = """/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr \
  -progress -nlt PROMOTE_TO_MULTI \
  -f "PostgreSQL" \
  PG:"host=localhost port=5432 dbname=urbis user=postgres password=postgres" \
  -nln tigerlineplaces \
  -lco SCHEMA=urbanclusters \
  -s_srs EPSG:3857 -t_srs EPSG:3857 \
  -lco OVERWRITE=YES \
  data/tigerlineplaces3857.shp """

pipe = Popen(args, stdout=PIPE, shell=True)
text = pipe.communicate()[0]


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



