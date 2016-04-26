# -*- coding: utf-8 -*-
import os

__all__ = (
    "build_report",
    "build_report_database",
    "setup_report",
)

base_path = os.path.abspath(os.path.dirname(__file__))

from .report import build_report, build_report_database
from .faces import project_faces_to_mollweide
from .graphics import plot_all_rows

def setup_report():
    print("Projecting")
    project_faces_to_mollweide()
    print("Plotting all RoW charts")
    plot_all_rows()
