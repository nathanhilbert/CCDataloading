find $URBIS_DATA/HSIP_GOLD_2015/Data -name \*.gdb -print0 | \
  time xargs -0 -n1 -t \
    ogr2ogr \
      -progress \
      -f "PostgreSQL" \
      PG:"host=ontoserv port=5432 dbname=urbis user=urbis password=urbis" \
      -lco SCHEMA=hsip2015 \
      -lco OVERWRITE=YES \
      -skipfailures \
  2>&1 | tee import-$(date +%Y-%m-%dT%H:%m).log