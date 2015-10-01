census-shape-download
========

Downloading US census shapefiles.
Code modified from: https://vvanhee.wordpress.com/2012/01/25/download-all-u-s-census-block-shapefiles/

Running the script will download the zip files from the US census site, put it into subfolders in the folder of the python script, unzip the zip file, 
and delete the original zip file. If [ogr2ogr](http://www.gdal.org/ogr2ogr.html) is installed, you can also add the option to convert shapefile to geojson.

Running example: 

`python census_shapefile_download.py --year 2012 --geolevel bg --state DC MD VA --json`

This line will download shapefiles for block group (bg), for states of DC, MA and VA, for the year of 2012. It will unzip the shapefiles to geojson and keep both shapefiles and geojson in separate folders.

Type `python census_shapefile_download.py --help` to get arguments available to pass in the command line.

If you need to download multiple year or geo-levels, use the shell script `census_shapefile_download.sh`.
