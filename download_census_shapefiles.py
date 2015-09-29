'''
Downloading US census shapefiles in one shot
Code modified from: https://vvanhee.wordpress.com/2012/01/25/download-all-u-s-census-block-shapefiles/

Running the script will download the zip files from the US census site, 
put it into subfolders in the folder of the python script,unzip the zip file, 
and delete the original zip file.

To run, type in the following command into the command line:

python download_census_shapefiles.py 

optional arguments:
  -h, --help            show this help message and exit
  -y, --year {2010,2011,2012,2013,2014,2015}
                        Download year (Choose single year between 2010 and 2015)
  -g, --geolevel {tract,bg,tabblock}
                        Geographical level (Choose between tract, bg, tabblock)

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
import argparse

def require_dir(path):
    # This function make the directory if it doesn't exist already
    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errno != errno.EEXIST:
            raise
 
# Get the list of state names and codes. The file should exist in the same directory as the python code.
fips_csv = csv.DictReader(open('fips2.csv', 'rU'), dialect='excel') 
rootdir = os.path.dirname(os.path.abspath(__file__))

#read in arguments from the command line
parser = argparse.ArgumentParser(description='Download TIGER shape files from Census Bureau.')

#specify download year
parser.add_argument("-y", "--year", help="Download year (Choose single year between 2010 and 2015)", type=int,
                    # choices=['2010', '2011', '2012', '2013', '2014', '2015'], default='2014')
                    choices=range(2010, 2016), default=2014)

#specify whether to be strict about keys
parser.add_argument("-g", "--geolevel", help="Geographical level (Choose between tract, bg, tabblock)",
                    choices=['tract', 'bg', 'tabblock'], default='tract')

args = parser.parse_args()

if __name__ == "__main__":
        
    #start a timer...
    # t_start = datetime.datetime.now()

    for row in fips_csv:
        statecode = row['code'].zfill(2)
        if args.geolevel == 'tabblock':
            fileroot = 'tl_' + str(args.year) + '_' + statecode + '_' + args.geolevel + '10'
        else:
            fileroot = 'tl_' + str(args.year) + '_' + statecode + '_' + args.geolevel

        filename = fileroot + '.zip'
        filedir = os.path.join(rootdir, str(args.year), args.geolevel, fileroot)
        require_dir(filedir)

        url = 'http://www2.census.gov/geo/tiger/TIGER' + str(args.year)+ '/' + args.geolevel.upper() + '/' + filename
        print 'Getting ' + row['statename'] + ' ' + args.geolevel + ' shape file: ' + filename

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

    #finish the timer and show to user
    # t_end = datetime.datetime.now()

    # print("elapsed time = {0}".format(t_end - t_start), file=sys.stderr)
