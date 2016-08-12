import argparse
import sys
import os
import os.path as op

def getProgargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", help="Base folder of the tiles")
    parser.add_argument("--table", help="e.g. public.sometable")
    parser.add_argument("--create", help="create database?", action="store_true", default=True)
    parser.add_argument("--numinserts", help="number of inserts at one time", default=350)
    parser.add_argument("--extrasql", default=None)
    parser.add_argument("--postgresuri", default='postgresql://urbis:urbis@localhost:5432/urbis')
    return parser.parse_args() 

if __name__ == '__main__':
    progargs = getProgargs()

    if not progargs.folder:
        print "ERROR: need a base folder of tiles"
        sys.exit()
    if not op.exists(progargs.folder):
        print "ERROR: Could not find folder specifed"
        sys.exit()
    if not progargs.table:
        print "ERROR: need a --table"
        sys.exit()

    if progargs.create:
        createfirst = True
    else:
        createfirst = False

    queue = []
    for f in os.listdir(progargs.folder):
        if not f.endswith('tif'):
            continue

        








    for FILEPATH in /data/nlcd/impervious/${YEAR} 
    do
        raster2pgsql -s 3857 -R -a -F -b 1  -N -f raster $FILEPATH landcover.nlcdimpervious |psql -U postgres -d urbis
        psql -d urbis -U postgres -c "UPDATE landcover.nlcdimpervious SET year=${YEAR} WHERE filename LIKE 'nlcd_impervious_${YEAR}%'"
    done


