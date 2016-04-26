# -*- coding: utf-8 -*-
from bw2regional.ecoinvent import discretize_rest_of_world
import collections
import jinja2
import os
import shutil


base_path = os.path.abspath(os.path.dirname(__file__))

# One table with RoWs as headings and excluded stuff as details
# One table with Activities and ref. products with RoW labels as details

def build_report(db_name):
    try:
        shutil.rmtree(os.path.join(base_path, "output"))
    except:
        pass
    os.mkdir(os.path.join(base_path, "output"))
    shutil.copytree(
        os.path.join(base_path, "data", "assets"),
        os.path.join(base_path, "output", "assets")
    )
    template = jinja2.Template(open(os.path.join(base_path, "data", "templates", "rows.html")).read())

    activity_dict, row_locations, locations, exceptions = discretize_rest_of_world(db_name, warn=False)

    counter = collections.defaultdict(int)
    for location in locations.values():
        counter[location] += 1

    data = [{
        'label': label,
        'count': counter[row],
        'exclusions': ", ".join(row)
    } for row, label in row_locations]

    with open(os.path.join(base_path, "output", "index.html"), "w") as f:
        f.write(template.render(rows=data, db=db_name))




# Convert NaturalEarthData raster to base map
# gdalwarp -s_srs 'EPSG:4326' -dstalpha -t_srs '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs' -ts 1000 500 GRAY_50M_SR_OB.tif base_map.tiff
# gdal_translate -of png base_map.tiff base_map.png
