from . import base_path
from .faces import faces_for_exclusions
from descartes import PolygonPatch
from PIL import Image
from shapely.geometry.multipolygon import MultiPolygon
import matplotlib.pyplot as plt
import os

BLUE = '#6699cc'


def add_geom(geom, axis):
    if isinstance(geom, MultiPolygon):
        for poly in geom:
            patch = PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.8, zorder=1, lw=0)
            axis.add_patch(patch)
    else:
        patch = PolygonPatch(geom, fc=BLUE, ec=BLUE, alpha=0.8, zorder=1, lw=0)
        axis.add_patch(patch)


def plot_row(label, exclusions):
    plt.figure(figsize=(5, 2.5))
    ax = plt.axes([0,0,1,1], frameon=False)
    ax.set_axis_off()

    for geom in faces_for_exclusions(exclusions):
        add_geom(geom, ax)

    image = Image.open(os.path.join(base_path, "data", "image", "base_map.png"))
    plt.imshow(
        image,
        zorder=0,
        extent=[-18040090.191, 18040093.456, -9020045.646, 9020047.848],
    )
    plt.savefig('output-{}.png'.format(label), dpi=200)
