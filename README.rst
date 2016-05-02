Ecoinvent RoW Report
====================

Tools to build an HTML report explaining what each "Rest of the World" location used in ecoinvent 3 means.

Report generation
-----------------

First, setup the necessary data by calling ``setup_report()``.

Then create a new `Brightway2 <https://brightwaylca.org/>`__ project with each version of ecoinvent you want to include. Ecoinvent databases should have the string "ecoinvent" (case-insensitive) in their name.

Finally, call ``ecoinvent_row_report.build_report("project name")`` to build the RoWs report.

Alternatively, call ``build_report_database("database name")`` to generate a RoWs report for a specific database.

Rest of World topologies
------------------------

The functions ``build_geopackage()`` and ``build_topomapping()`` can be used to generate the data needed for `Brightway2-regional <https://bitbucket.org/cmutel/brightway2-regional>`__ geo- and topocollections.

Base world map
--------------

The base world map was created from the `natural earth data <http://www.naturalearthdata.com/>`__ `50m gray earth <http://www.naturalearthdata.com/downloads/50m-raster-data/50m-gray-earth>`__ raster image using the following `GDAL <http://www.gdal.org/>`__ commands:

.. code-block:: bash

    gdalwarp -s_srs 'EPSG:4326' -dstalpha -t_srs '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs' -ts 1000 500 GRAY_50M_SR_OB.tif base_map.tiff
    gdal_translate -of png base_map.tiff base_map.png
