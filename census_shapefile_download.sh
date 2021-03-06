#!/bin/sh
# This shell script will run the census_shapefile_download.py to download shape files from census bureau site.
# Modify the arguments in for-loop or the python call itself to suit what you need.

for g in tract
do
    for y in 2010 2011 2012 2013
    do
        python census_shapefile_download.py --year $y --geolevel $g --s CA NY --json
    done
done
