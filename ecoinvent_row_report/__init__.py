# -*- coding: utf-8 -*-
from bw2regional.ecoinvent import discretize_rest_of_world
import collections
import jinja2
import os
import shutil


base_path = os.path.abspath(os.path.dirname(__file__))

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
