from . import base_path
from constructive_geometries import ConstructiveGeometries
from pandarus.projection import project, MOLLWEIDE
from shapely.geometry import shape, mapping
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
import fiona
import os
import json

cg = ConstructiveGeometries()


def _(geom):
    if isinstance(geom, Polygon):
        return MultiPolygon([geom])
    return geom


def project_faces_to_mollweide():
        if not os.path.exists(os.path.join(base_path, "data", "faces")):
            os.mkdir(os.path.join(base_path, "data", "faces"))

        meta = {
            'crs': {'no_defs': True, 'ellps': 'WGS84', 'datum': 'WGS84',
                    'proj': 'moll', 'lon_0': '0', 'x_0': '0', 'y_0': '0',
                    'units': 'm'},
            'driver': 'GPKG',
            'schema': {'geometry': 'MultiPolygon', 'properties': {'id': 'int'}}
        }
        fp = os.path.join(base_path, "data", "faces", "faces.gpkg")

        with fiona.drivers():
            data = []
            with fiona.open(cg.faces_fp) as src:
                for feat in src:
                    data.append((
                        feat['properties']['id'],
                        project(shape(feat['geometry']), to_proj=MOLLWEIDE)
                    ))
            with fiona.open(fp, 'w', **meta) as sink:
                for label, geom in data:
                    sink.write({
                        'geometry': mapping(_(geom)),
                        'properties': {'id': label}
                    })


def faces_for_exclusions(exclusions):
    faces_mapping = dict(json.load(open(cg.data_fp)))
    excluded = {x for label in exclusions for x in faces_mapping[label]}
    geoms = []

    with fiona.drivers():
        with fiona.open(os.path.join(base_path, "data", "faces", "faces.gpkg")) as src:
            for feat in src:
                if feat['properties']['id'] not in excluded:
                    geoms.append(shape(feat['geometry']))

    return geoms
