#!/bin/sh
# This shell script will run the census2text2010.py to download data from census bureau site
# Tables of interest:
#   P1: Total population 
#   P12: Population break down by age and sex bins
# Geography levels of interest: county, tract, blockgroup

echo "start time: `date`"

for g in bg tract
do
    for y in 2010 2011 2012 2013 2014
    do
        python census_shapefile_download.py --year $y --geolevel $g --s DC MD VA
    done
done

echo "end time: `date`"