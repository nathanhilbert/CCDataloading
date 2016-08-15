
# coding: utf-8

# In[2]:

from sqlalchemy import create_engine


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BIGINT
from geoalchemy2 import Geometry, Raster, RasterElement
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://urbis:urbis@localhost:5432/urbis', poolclass=NullPool)



# In[8]:



TABLES = {'regtiles': 'population.landscan',
         'regfullintotiles': 'population.landscantiled',
         'loadedtiles': 'population.landscanloadedtile'}

for ind, table in TABLES.iteritems():
    
    r = engine.execute("""SELECT pg_size_pretty(pg_total_relation_size('{0}')) As fulltblsize;""".format(table))
    for p in r:
        print "\t\tDiskSize:", p[0]
        

    
    


# In[ ]:

import time
for ind, table in TABLES.iteritems():
    print ind
    manyclusterstatssql = """SELECT neurban.id as urbanid , ST_SummaryStats(ST_Clip( 
        (SELECT ST_Union(raster) FROM {0} as landscan WHERE ST_Intersects(landscan.raster, 
        ST_Transform(ST_SetSRID(neurban.geom,4326), 3857))
        GROUP BY neurban.id) ,1, 
        ST_Transform(ST_SetSRID(neurban.geom,4326), 3857), true)) 
        FROM urbanclusters.natearth_urbanareas_10m as neurban, urbanclusters.tigerlineplaces as tplace 
        WHERE St_Intersects(neurban.geom, tplace.geom) 
        GROUP BY neurban.id """.format(table)
    
    clusterstarttime = time.time()
    r2 = engine.execute(manyclusterstatssql)
    print "\t\tManyClusters Took", time.time() - clusterstarttime, "seconds"


# In[ ]:

import time
for ind, table in TABLES.iteritems():
    print ind
    manyclusterstatssql = """SELECT neurban.id as urbanid , ST_SummaryStats(ST_Clip( 
        (SELECT ST_Union(raster) FROM {0} as landscan 
        WHERE ST_Intersects(landscan.raster, 
        ST_Transform(ST_SetSRID(neurban.geom,4326), 3857))
        GROUP BY neurban.id) ,1, 
        ST_Transform(ST_SetSRID(neurban.geom,4326), 3857), true)) 
        FROM urbanclusters.natearth_urbanareas_10m as neurban, urbanclusters.tigerlineplaces as tplace 
        WHERE St_Intersects(neurban.geom, tplace.geom) AND neurban.id IN (2026, 2024, 4083)
        GROUP BY neurban.id """.format(table)
    
    clusterstarttime = time.time()
    r2 = engine.execute(manyclusterstatssql)
    print "\t\tFewClusters Took", time.time() - clusterstarttime, "seconds"


