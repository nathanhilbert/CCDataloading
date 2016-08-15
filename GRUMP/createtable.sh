psql -U postgres -d urbis -c "CREATE TABLE population.landscan  \
( \
  rid serial NOT NULL, \
  raster raster, \
  filename text, \
   year integer, \
  CONSTRAINT landscan_pkey PRIMARY KEY (rid) \
) \
WITH ( \
  OIDS=FALSE \
); \
ALTER TABLE population.landscan \
  OWNER TO postgres"