Ecoinvent RoW Report
====================

Tools to build an HTML report explaining what each "Rest of the World" location used in ecoinvent 3 means.

Usage
-----

First, project the ``constructive_geometries`` topographical faces be calling ``ecoinvent_row_report.project_faces_to_mollweide()``.

Then create a new `Brightway2 <https://brightwaylca.org/>`__ project with each version of ecoinvent you want to include. Ecoinvent databases should have the string "ecoinvent" (case-insensitive) in their name.

Finally, call ``ecoinvent_row_report.build_report(project_name)`` to build the RoWs report.

Base world map
--------------

The base world map was created from the `natural earth data <http://www.naturalearthdata.com/>`__ `50m gray earth <http://www.naturalearthdata.com/downloads/50m-raster-data/50m-gray-earth>`__ raster image using the following `GDAL <http://www.gdal.org/>`__ commands:

.. code-block:: bash

    gdalwarp -s_srs 'EPSG:4326' -dstalpha -t_srs '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs' -ts 1000 500 GRAY_50M_SR_OB.tif base_map.tiff
    gdal_translate -of png base_map.tiff base_map.png
