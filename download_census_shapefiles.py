'''
Downloading US census shapefiles in one shot
Code modified from: https://vvanhee.wordpress.com/2012/01/25/download-all-u-s-census-block-shapefiles/

Running the script will download the zip files from the US census site, 
put it into subfolders in the folder of the python script,unzip the zip file, 
and delete the original zip file.

To run, type in the following command into the command line:

python download_census_shapefiles.py [level]

The level argument can take on one of the three values. Default to 'tract' if the arg is not specified.
    tract: census tract
    bg: census block groups
    tabblocks: census blocks
'''

import urllib
import csv
import sys
import os
import errno

year = '2014'

def require_dir(path):
    # This function make the directory if it doesn't exist already
    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errno != errno.EEXIST:
            raise

if len(sys.argv) > 1:
    if sys.argv[1].lower() in ['tract', 'bg', 'tabblock']:
        level = sys.argv[1].lower()
    else:
        print 'Error: accepted levels are "tract", "bg", or "tabblock".'
        exit(1)
else:
    level = 'tract' # default to download tract data if it is not specified in sys.argv
 
# Get the list of state names and codes. The file should exist in the same directory as the python code.
fips_csv = csv.DictReader(open('fips.csv', 'rU'), dialect='excel') 
rootdir = os.path.dirname(os.path.abspath(__file__))
 
for row in fips_csv:
    statecode = row['code'].zfill(2)
    if level == 'tabblock':
        fileroot = 'tl_' + year + '_' + statecode + '_' + level + '10'
    else:
        fileroot = 'tl_' + year + '_' + statecode + '_' + level

    filename = fileroot + '.zip'
    filedir = os.path.join(rootdir, level, fileroot)
    require_dir(filedir)

    url = 'http://www2.census.gov/geo/tiger/TIGER' + year + '/' + level.upper() + '/' + filename
    print 'Getting ' + row['statename'] + ' ' + level + ' shape file: ' + filename

    try:
        urllib.urlretrieve(url, os.path.join(filedir, filename))

        # Comment out the following code block if you do not wish to unzip the files
        os.chdir(filedir)
        os.system('unzip ' + os.path.join(filedir, filename))
        os.system('rm ' + os.path.join(filedir, filename))
        os.chdir(rootdir)
        #

    except:
        print "Unexpected error:", sys.exc_info()[0]
        sys.exc_clear()
