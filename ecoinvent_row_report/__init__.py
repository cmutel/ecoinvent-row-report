# -*- coding: utf-8 -*-

# from .report import build_report, build_report_database
import os
import appdirs

__all__ = (
    "RoWGrapher",
    "Report",
)
__version__ = (0, 2)

DEFAULT_MAPPING = { # Database name: Display name
    '3.3 apos': 'ecoinvent 3.3 APOS',
    '3.3 consequential': 'ecoinvent 3.3 consequential',
    '3.3 cutoff': 'ecoinvent 3.3 cutoff',
    '3.4 apos': 'ecoinvent 3.4 APOS',
    '3.4 consequential': 'ecoinvent 3.4 consequential',
    '3.4 cutoff': 'ecoinvent 3.4 cutoff',
}

DATADIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")
CACHEDIR = os.path.abspath(appdirs.user_data_dir("row-report", "row-reporter"))

from constructive_geometries import ConstructiveGeometries
cg = ConstructiveGeometries()
cg.load_definitions()

from .graphics import RoWGrapher
from .report import Report
