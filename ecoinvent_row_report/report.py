from bw2regional.ecoinvent import discretize_rest_of_world
import collections
import jinja2
import os
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
    shutil.copytree(
        os.path.join(base_path, "data", "assets"),
        os.path.join(base_path, "output", "assets")
    )


def build_report():
    # TODO - for entire project
    pass


def build_report_database(db_name):
    prepare_output_dir()
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
