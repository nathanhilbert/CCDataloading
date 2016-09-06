DROPVIEW = """DROP MATERIALIZED VIEW urbanclusters.{0} CASCADE"""

BASEVIEW = """ 
CREATE MATERIALIZED VIEW urbanclusters.{0} AS 
WITH places AS (
         SELECT neurban.ogc_fid AS id,
            (array_agg(tplace.name ORDER BY pop.populationtotal DESC))[1] AS placename,
            (array_agg(tplace.ogc_fid ORDER BY pop.populationtotal DESC))[1] AS placeid,
            neurban.wkb_geometry AS geom
           FROM urbanclusters.{1} neurban,
            urbanclusters.tigerlineplaces tplace,
            population.censuspopulation as pop
          WHERE st_intersects(neurban.wkb_geometry, tplace.wkb_geometry) AND 
        pop.geoidreal=tplace.geoidreal
          GROUP BY neurban.ogc_fid
        )
 SELECT max(places.id) AS id,
    places.placeid,
    places.placename,
    st_union(places.geom) AS geom
   FROM places
  GROUP BY places.placeid, places.placename
WITH DATA;"""

SETOWNER = """
ALTER TABLE urbanclusters.{0}
  OWNER TO urbis;"""

SETINDEX  = """CREATE INDEX {0}_geom_idx
  ON urbanclusters.{0}
  USING gist
  (geom);"""


from sqlalchemy import create_engine


tables = {
    'earthenvurbanextent': 'earthenv_urbannamed',
    'globcoverurbanextent': 'globcover_urbannamed',
    'grumpurbanextents': 'grump_urbannamed',
    'landscanurbancluster': 'landscan_urbannamed',
    'ne_10m_urban_areas': 'ne_10m_urbannamed'
}

POSTGRESURI = 'postgresql://urbis:urbis@localhost:5432/urbis'
engine = create_engine(POSTGRESURI)

try:
    engine.execute(DROPVIEW.format('cityoptions'))
except Exception,e:
    print e


for table, viewname in tables.iteritems():
    basesql = BASEVIEW.format(viewname, table)
    setownersql = SETOWNER.format(viewname)
    setindexsql = SETINDEX.format(viewname)
    try:
        engine.execute(DROPVIEW.format(viewname))
    except Exception,e:
        print e

    try:
        engine.execute(basesql)
        engine.execute(setownersql)
        engine.execute(setindexsql)
    except Exception,e:
        print e


uniontables = ["""SELECT urbanclusters.{0}.placename,
            urbanclusters.{0}.placeid
           FROM urbanclusters.{0}""".format(t) for t in tables.values()]

placeoptions = """CREATE MATERIALIZED VIEW urbanclusters.cityoptions AS 
 WITH cities AS (
         {0}
        )
 SELECT DISTINCT cities.placename,
    cities.placeid,
    (cities.placename::text || ', '::text) || tlstates.name::text AS label
   FROM cities
     LEFT JOIN urbanclusters.tigerlineplaces tlplaces ON cities.placeid = tlplaces.ogc_fid
     LEFT JOIN urbanclusters.tigerlinestates tlstates ON tlplaces.statefp::text = tlstates.statefp::text
WITH DATA;

ALTER TABLE urbanclusters.cityoptions
  OWNER TO urbis;


CREATE INDEX cityoptions_city_search_idx
  ON urbanclusters.cityoptions
  USING btree
  (label COLLATE pg_catalog."default");""".format(" UNION ALL ".join(uniontables))

engine.execute(placeoptions)
