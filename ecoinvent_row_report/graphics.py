from constructive_geometries import ConstructiveGeometries
from descartes import PolygonPatch
from pandarus.projection import project, MOLLWEIDE
from PIL import Image
from shapely.geometry.multipolygon import MultiPolygon
import matplotlib.pyplot as plt
import os

BLUE = '#6699cc'


def plot_row(label, exclusions):
    base_path = os.path.abspath(os.path.dirname(__file__))

    cg = ConstructiveGeometries()

    plt.figure(figsize=(5, 2.5))
    ax = plt.axes([0,0,1,1], frameon=False)
    ax.set_axis_off()

    # plt.scatter(x,y,zorder=1)
    geom = cg.construct_rest_of_world(exclusions)
    geom = project(geom, to_proj=MOLLWEIDE)
    if isinstance(geom, MultiPolygon):
        for poly in geom:
            patch = PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.8, zorder=1)
            ax.add_patch(patch)
    else:
        patch = PolygonPatch(geom, fc=BLUE, ec=BLUE, alpha=0.8, zorder=1)
        ax.add_patch(patch)

    image = Image.open(os.path.join(base_path, "data", "image", "base_map.png"))
    plt.imshow(
        image,
        zorder=0,
        extent=[-18040090.191, 18040093.456, -9020045.646, 9020047.848],
    )
    plt.savefig('output-{}.png'.format(label), dpi=200)

