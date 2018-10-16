from . import DATADIR, cg
from .faces import projected_fp, project_faces_to_mollweide
from descartes import PolygonPatch
from PIL import Image
from shapely.geometry import shape
from shapely.geometry.multipolygon import MultiPolygon
import fiona
import json
import matplotlib.pyplot as plt
import os
import pyprind
import shutil


BLUE = '#6699cc'
IMAGE_PATH = os.path.join(DATADIR, "image", "base_map.png")


def add_geom(geom, axis):
    if isinstance(geom, MultiPolygon):
        for poly in geom:
            patch = PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.8, zorder=1, lw=0)
            axis.add_patch(patch)
    else:
        patch = PolygonPatch(geom, fc=BLUE, ec=BLUE, alpha=0.8, zorder=1, lw=0)
        axis.add_patch(patch)


class RoWGrapher:
    def __init__(self):
        if not os.path.exists(projected_fp):
            project_faces_to_mollweide()

        self.load_faces()

    def load_faces(self):
        self.faces = {}

        with fiona.drivers():
            with fiona.open(projected_fp) as src:
                for feat in src:
                    self.faces[feat['properties']['id']] = shape(feat['geometry'])

    def plot_row(self, exclusions, filepath):
        fig = plt.figure(figsize=(5, 2.5))
        ax = plt.axes([0,0,1,1], frameon=False)
        ax.set_axis_off()

        excluded = set()

        for region in exclusions:
            for face_id in cg.data[region]:
                excluded.add(face_id)

        for face_id in self.faces:
            if face_id not in excluded:
                add_geom(self.faces[face_id], ax)

        image = Image.open(IMAGE_PATH)
        plt.imshow(
            image,
            zorder=0,
            extent=[-18040090.191, 18040093.456, -9020045.646, 9020047.848],
        )
        plt.savefig(filepath, dpi=200)
        plt.close()
