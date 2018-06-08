from . import DEFAULT_MAPPING, DATADIR
from .graphics import RoWGrapher
from bw2data import databases, Database
import collections
import jinja2
import json
import os
import pyprind
import shutil
import rower
import constructive_geometries


class Report:
    def __init__(self, dirpath, mapping=DEFAULT_MAPPING, overwrite=False):
        if os.path.exists(dirpath) and not overwrite:
            raise OSError("Directory already exists")
        self.dirpath = dirpath
        self.mapping = mapping
        self.grapher = RoWGrapher()
        self.rows = self.load_rows()
        self.ecoinvents = {
            db: rower.RowerDatapackage(
                os.path.join(rower.DATAPATH, label)
            ).read_data()
            for db, label in self.mapping.items()
        }

    def make_report(self):
        self.prepare_output_dir()
        self.load_databases()
        self.get_global_counts()
        self.make_rows_index()
        print("Creating individual RoW reports")
        for label, exclusions in pyprind.prog_bar(self.rows.items()):
            self.make_row(label, exclusions)

    def prepare_output_dir(self):
        if os.path.exists(self.dirpath):
            shutil.rmtree(os.path.join(self.dirpath))

        os.makedirs(self.dirpath)
        shutil.copytree(
            os.path.join(DATADIR, "assets"),
            os.path.join(self.dirpath, "assets")
        )

    def load_rows(self):
        obj = rower.RowerDatapackage(
            os.path.join(rower.DATAPATH, "ecoinvent generic")
        )
        return obj.read_data()["Rest-of-World definitions"]

    def load_databases(self):
        ds = lambda x: (x['name'], x['reference product'], x['unit'])

        self.databases = {}
        for db in self.mapping:
            if db in databases:
                print("Loading:", db)
                self.databases[db] = {
                    act['code']: ds(act) for act in Database(db)
                }

    def get_global_counts(self):
        self.counts = collections.defaultdict(int)
        for obj in self.ecoinvents.values():
            for label, lst in obj["Activity mapping"].items():
                self.counts[label] += len(lst)

    def make_rows_index(self):
        shorten = lambda x: x[:60] + "..." if len(x) > 60 else x

        data = {
            'cg_version': constructive_geometries.__version__,
            'rower_version': rower.__version__,
            'ecoinvents': self.mapping.values(),
            'rows': [{
                'number': int(label.replace("RoW_", "")),
                'url': label + '.html',
                'label': label,
                'count': self.counts[label],
                'exclusions': shorten("|".join(lst))
            } for label, lst in self.rows.items()]
        }

        template = jinja2.Template(open(os.path.join(DATADIR, "templates", "rows.html")).read())
        with open(os.path.join(self.dirpath, "index.html"), "w") as f:
            f.write(template.render(**data))

    def make_row(self, label, exclusions):
        self.grapher.plot_row(
            exclusions,
            os.path.join(self.dirpath, "output-{}.png".format(label))
        )

        databases = [{
            'label': self.mapping[key],
            'activities': [
                self.databases[key][code]
                for code in dct["Activity mapping"].get(label, [])
            ]
        } for key, dct in self.ecoinvents.items()]

        data = {
            'cg_version': constructive_geometries.__version__,
            'rower_version': rower.__version__,
            'label': label,
            'excluded': ', '.join(exclusions),
            'databases': [x for x in databases if x['activities']]
        }

        template = jinja2.Template(open(os.path.join(DATADIR, "templates", "row.html")).read())
        with open(os.path.join(self.dirpath, "{}.html".format(label)), "w") as f:
            f.write(template.render(**data))
