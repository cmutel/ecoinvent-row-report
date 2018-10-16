Ecoinvent RoW Report
====================

Tools to build an HTML report explaining what each "Rest of the World" location used in ecoinvent 3 means.

Usage
-----

import ecoinvent_row_report as e
from brightway2 import projects
projects.set_current("RoW generation")  # Project with all ecoinvents
r = e.Report("Absolute filepath to output directory to be created")
r.make_report()

Upload to geography.ecoinvent.org server
----------------------------------------

cd output_directory
rsync -zv *.* 129.132.117.28:websites/geography.ecoinvent.org/rows/
rsync -rzv assets 129.132.117.28:websites/geography.ecoinvent.org/rows/assets

Base world map
--------------

The base world map was created from the `natural earth data <http://www.naturalearthdata.com/>`__ `50m gray earth <http://www.naturalearthdata.com/downloads/50m-raster-data/50m-gray-earth>`__ raster image using the following `GDAL <http://www.gdal.org/>`__ commands:

.. code-block:: bash

    gdalwarp -s_srs 'EPSG:4326' -dstalpha -t_srs '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs' -ts 1000 500 GRAY_50M_SR_OB.tif base_map.tiff
    gdal_translate -of png base_map.tiff base_map.png
