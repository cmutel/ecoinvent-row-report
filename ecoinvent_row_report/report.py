from . import base_path
from bw2regional.ecoinvent import discretize_rest_of_world
import collections
import jinja2
import json
import os
import pyprind
import shutil

# Rest of Worlds

# - Table of Rows
# - Link to each RoW detail page
# - Expand: See all geos excluded
# - Link to other ecoinvent versions/all
# - Count of numbers of times used

def prepare_output_dir():
    try:
        shutil.rmtree(os.path.join(base_path, "output"))
    except:
        pass
    os.mkdir(os.path.join(base_path, "output"))
    os.mkdir(os.path.join(base_path, "output", "row"))
    shutil.copytree(
        os.path.join(base_path, "data", "assets"),
        os.path.join(base_path, "output", "assets")
    )
    shutil.copytree(
        os.path.join(base_path, "data", "charts"),
        os.path.join(base_path, "output", "assets", "images")
    )


def build_report():
    # TODO - for entire project
    pass


def build_report_database(db_name):
    prepare_output_dir()

    standard_definitions = {frozenset(v): k for k, v in json.load(open(os.path.join(base_path, "data", "rows-ecoinvent.json")))}

    activity_dict, row_locations, locations, exceptions = discretize_rest_of_world(db_name, warn=False)
    row_locations = {
        tuple(sorted(k)): standard_definitions[frozenset(k)]
        for k in dict(row_locations)
        if k
    }
    rl = dict(row_locations)

    counter = collections.defaultdict(int)
    for location in locations.values():
        if not location:
            continue
        counter[location] += 1

    reverse_locations = {}
    for k, v in locations.items():
        if not v:
            continue
        reverse_locations[rl[v]] = reverse_locations.get(rl[v], []) + [k]

    data = [{
        'label': label,
        'number': label.replace("RoW-", ""),
        'count': counter[row],
        'url': "row/" + label + '.html',
        'exclusions': ", ".join(row)
    } for row, label in row_locations.items()]

    template = jinja2.Template(open(os.path.join(base_path, "data", "templates", "rows.html")).read())
    with open(os.path.join(base_path, "output", "index.html"), "w") as f:
        f.write(template.render(rows=data, db=db_name))

    template = jinja2.Template(open(os.path.join(base_path, "data", "templates", "row.html")).read())

    for row, label in pyprind.prog_bar(row_locations.items()):
        with open(os.path.join(base_path, "output", "row", label + ".html"), "w") as f:
            f.write(template.render(
                label=label,
                rows=reverse_locations[label],
                excluded=", ".join(row)
            ))
