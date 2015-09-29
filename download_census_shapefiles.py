'''
Downloading US census shapefiles in one shot
Code modified from: https://vvanhee.wordpress.com/2012/01/25/download-all-u-s-census-block-shapefiles/

Running the script will download the zip files from the US census site, 
put it into subfolders in the folder of the python script,unzip the zip file, 
and delete the original zip file.

To run, type in the following command into the command line:

python download_census_shapefiles.py 

optional arguments:
  -h, --help: Show this help message and exit
  -y, --year: Download year (Choose single year between 2010 and 2015)
  -g, --geolevel: Geographical level (Choose between tract, bg, tabblock)
  -s, --state: State(s) that you want to download the shape files for. Use two-character abbreviations, eg. --state DC MD VA
  -z, --zip: Keep files in zipped format. Default is to unzip.

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

# Dictionary to convert two-letter state to fips codes
states = {'AK': '02', 'AL': '01', 'AR': '05', 'AS': '60', 'AZ': '04', 'CA': '06', 
          'CO': '08', 'CT': '09', 'DC': '11', 'DE': '10', 'FL': '12', 'GA': '13', 
          'GU': '66', 'HI': '15', 'IA': '19', 'ID': '16', 'IL': '17', 'IN': '18', 
          'KS': '20', 'KY': '21', 'LA': '22', 'MA': '25', 'MD': '24', 'ME': '23', 
          'MI': '26', 'MN': '27', 'MO': '29', 'MP': '69', 'MS': '28', 'MT': '30', 
          'NC': '37', 'ND': '38', 'NE': '31', 'NH': '33', 'NJ': '34', 'NM': '35', 
          'NV': '32', 'NY': '36', 'OH': '39', 'OK': '40', 'OR': '41', 'PA': '42', 
          'PR': '72', 'RI': '44', 'SC': '45', 'SD': '46', 'TN': '47', 'TX': '48', 
          'UT': '49', 'VA': '51', 'VI': '78', 'VT': '50', 'WA': '53', 'WI': '55', 
          'WV': '54', 'WY': '56'
         }

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

parser.add_argument("-s", "--state", help="State(s) that you want to download the shape files for. \
                    Use two-character abbreviations, eg. --state DC MD VA", 
                    nargs='*', choices=states.keys())

parser.add_argument("-z", "--zip", help="Keep files in zipped format. Default is to unzip.", action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
        
    for state in args.state:
        statecode = states[state]
        if args.geolevel == 'tabblock':
            fileroot = 'tl_' + str(args.year) + '_' + statecode + '_' + args.geolevel + '10'
        else:
            fileroot = 'tl_' + str(args.year) + '_' + statecode + '_' + args.geolevel

        filename = fileroot + '.zip'
        filedir = os.path.join(rootdir, str(args.year), args.geolevel, fileroot)
        require_dir(filedir)

        url = 'http://www2.census.gov/geo/tiger/TIGER' + str(args.year)+ '/' + args.geolevel.upper() + '/' + filename
        print 'Getting ' + state + ' ' + args.geolevel + ' shape file: ' + filename

        try:
            urllib.urlretrieve(url, os.path.join(filedir, filename))

            if not args.zip:
                os.chdir(filedir)
                os.system('unzip ' + os.path.join(filedir, filename))
                os.system('rm ' + os.path.join(filedir, filename))
                os.chdir(rootdir)

        except:
            print "Unexpected error:", sys.exc_info()[0]
            sys.exc_clear()
