'''
Downloading US census shapefiles in one shot
Code modified from: https://vvanhee.wordpress.com/2012/01/25/download-all-u-s-census-block-shapefiles/

Running the script will download the zip files from the US census site, 
put it into subfolders in the folder of the python script, unzip the zip file, 
and delete the original zip file.

Running example: 

python census_shapefile_download.py --year 2012 --geolevel bg --state DC MD VA --json

This line will download shapefiles for block group (bg), for states of DC, MA and VA, for the year of 2012. 
It will unzip the shapefiles to geojson and keep both shapefiles and geojson in separate folders.

required arguments:
  -s, --state: State(s) that you want to download the shape files for. Use two-character abbreviations, eg. --state DC MD VA

optional arguments:
  -h, --help: Show this help message and exit
  -y, --year: Download year (Choose single year between 2010 and 2015). Default to 2014.
  -g, --geolevel: Geographical level (Choose between tract, bg, tabblock). Default to tract.
  -z, --zip: Keep files in zipped format. Default is false (ie. will unzip).
  -j, --json: Convert shapefile to json. Requires ogr2ogr installed on the system. Default is to not convert. 

The level argument can take on one of the three values. Default to 'tract' if the arg is not specified.
    tract: census tract
    bg: census block groups
    tabblocks: census blocks
'''

import urllib
import sys
import os
import errno
import argparse
import subprocess

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

rootdir = os.path.dirname(os.path.abspath(__file__))

# Read in arguments from the command line
parser = argparse.ArgumentParser(description='Download TIGER shape files from Census Bureau.')

# Specify download year
parser.add_argument("-y", "--year", help="Download year (Choose single year between 2010 and 2015)", type=int,
                    choices=range(2010, 2016), default=2014)

# Specify geo-level
parser.add_argument("-g", "--geolevel", help="Geographical level (Choose between tract, bg, tabblock)",
                    choices=['tract', 'bg', 'tabblock'], default='tract')

# Specify state(s) by two-character abbreviations
parser.add_argument("-s", "--state", help="State(s) that you want to download the shape files for. \
                    Use two-character abbreviations, eg. --state DC MD VA", 
                    nargs='*', choices=states.keys())

# Specify whether to unzip (Unzip will occur by default)
parser.add_argument("-z", "--zip", help="Keep files in zipped format. Default is to unzip.", action="store_true")

# Specify whether to convert shape file to geojson. 
# Requires ogr2ogr to be installed on the system to work. See http://www.gdal.org/ogr2ogr.html

parser.add_argument("-j", "--json", help="Convert shapefile to json. Default is to not convert. \
                    Note: requires ogr2ogr (http://www.gdal.org/ogr2ogr.html) installed on the system.", action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
        
    for state in args.state:
        statecode = states[state]

        # The multiple if-else blocks is necessary to navigate the folder structure of census ftp site.
        # Adding more supported year or geo-levels will require significant refactoring of this code.

        if args.year >= 2014:
            if args.geolevel == 'tabblock':
                fileroot = 'tl_' + str(args.year) + '_' + statecode + '_' + args.geolevel + '10'
            else:
                fileroot = 'tl_' + str(args.year) + '_' + statecode + '_' + args.geolevel

            filename = fileroot + '.zip'
            url = 'http://www2.census.gov/geo/tiger/TIGER' + str(args.year)+ '/' + args.geolevel.upper() + '/' + filename

        elif args.year >= 2011 and args.year < 2014:
            fileroot = 'tl_' + str(args.year) + '_' + statecode + '_' + args.geolevel
            filename = fileroot + '.zip'
            url = 'http://www2.census.gov/geo/tiger/TIGER' + str(args.year)+ '/' + args.geolevel.upper() + '/' + filename

        elif args.year == 2010:
            fileroot = 'tl_' + str(args.year) + '_' + statecode + '_' + args.geolevel + '10'
            filename = fileroot + '.zip'
            url = 'http://www2.census.gov/geo/tiger/TIGER' + str(args.year)+ '/' + args.geolevel.upper() + '/' + str(args.year) + '/' + filename

        # Make shapefile/ and geojson/ folders if it doesn't exist already
        filedir = os.path.join(rootdir, 'shapefile')
        require_dir(filedir)
        if args.json:
            require_dir(os.path.join(rootdir, 'geojson'))

        print 'Getting ' + state + ' ' + args.geolevel + ' shape file: ' + filename

        try:
            urllib.urlretrieve(url, os.path.join(filedir, filename))

            # unzip unless specified otherwise, and remove zip file
            if not args.zip:
                os.chdir(filedir)
                subprocess.call('unzip ' + os.path.join(filedir, filename) + ' -d ' + fileroot, shell=True)
                subprocess.call('rm ' + os.path.join(filedir, filename), shell=True)
                os.chdir(rootdir)

                # convert to geojson - requires ogr2ogr installed on the system. 
                if args.json:
                    subprocess.call('ogr2ogr -f GeoJSON -t_srs crs:84 ' + \
                        os.path.join(rootdir, 'geojson', fileroot) + '.geojson ' + \
                        os.path.join(filedir, fileroot, fileroot) + '.shp', shell=True)

            # if user only want geojson but not unzip, then unzip to a subfolder, 
            # convert the shapefile to json, then delete the subfolder that contain unzipped files
            if args.zip and args.json:
                os.chdir(filedir)
                subprocess.call('unzip ' + os.path.join(filedir, filename) + ' -d ' + fileroot, shell=True)
                os.chdir(rootdir)
                subprocess.call('ogr2ogr -f GeoJSON -t_srs crs:84 ' + \
                    os.path.join(rootdir, 'geojson', fileroot) + '.geojson ' + \
                    os.path.join(filedir, fileroot, fileroot) + '.shp', shell=True)
                subprocess.call('rm -rf ' + os.path.join(filedir, fileroot), shell=True)

        except:
            print "Unexpected error:", sys.exc_info()[0]
            sys.exc_clear()
