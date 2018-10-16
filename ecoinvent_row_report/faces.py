from . import CACHEDIR, cg
from .filesystem import md5
from pandarus.projection import project, MOLLWEIDE
from shapely.geometry import shape, mapping
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
import fiona
import os
import pyprind



projected_dir = os.path.join(CACHEDIR, md5(cg.faces_fp))
projected_fp = os.path.join(projected_dir, "faces.gpkg")
if not os.path.exists(projected_dir):
    os.makedirs(projected_dir)


def to_mp(geom):
    if isinstance(geom, Polygon):
        return MultiPolygon([geom])
    return geom


def project_faces_to_mollweide():
    print("Projecting topological faces to Mollweide projection")
    if os.path.exists(projected_fp):
        return

    meta = {
        'crs': {'no_defs': True, 'ellps': 'WGS84', 'datum': 'WGS84',
                'proj': 'moll', 'lon_0': '0', 'x_0': '0', 'y_0': '0',
                'units': 'm'},
        'driver': 'GPKG',
        'schema': {'geometry': 'MultiPolygon', 'properties': {'id': 'int'}}
    }

    with fiona.drivers():
        data = []
        with fiona.open(cg.faces_fp) as src:
            for feat in src:
                data.append((
                    feat['properties']['id'],
                    project(shape(feat['geometry']), to_proj=MOLLWEIDE)
                ))
        with fiona.open(projected_fp, 'w', **meta) as sink:
            for label, geom in pyprind.prog_bar(data):
                sink.write({
                    'geometry': mapping(to_mp(geom)),
                    'properties': {'id': label}
                })


# def faces_for_exclusions(exclusions):
#     faces_mapping = dict(cg.data)
#     excluded = {x for label in exclusions for x in faces_mapping[label]}
#     geoms = []

#     with fiona.drivers():
#         with fiona.open(os.path.join(base_path, "data", "faces", "faces.gpkg")) as src:
#             for feat in src:
#                 if feat['properties']['id'] not in excluded:
#                     geoms.append(shape(feat['geometry']))

#     return geoms


# def build_geopackage():
#     exclusions = dict(json.load(open(os.path.join(base_path, "data", "rows-ecoinvent.json"))))
#     fp = os.path.join(base_path, "data", "rows.gpkg")
#     cg.construct_rest_of_worlds(exclusions, fp)


# def build_topomapping():
#     exclusions = dict(json.load(open(os.path.join(base_path, "data", "rows-ecoinvent.json"))))
#     fp = os.path.join(base_path, "data", "rows-topomapping.json")
#     cg.construct_rest_of_worlds_mapping(exclusions, fp)
