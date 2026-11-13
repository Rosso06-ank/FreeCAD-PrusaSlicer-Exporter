# -*- coding: utf-8 -*-
"""
FreeCAD PrusaSlicer Exporter
---------------------------
FreeCAD Workbench Addon

Features:
- Export selected Body or Part
- Export selected Faces
- Export multiple objects
- Export without saving FreeCAD document
- Send STL files directly to PrusaSlicer

Workbench registration: InitGui.py
"""

import FreeCAD as App

App.Console.PrintLog(
    "[PrusaSlicer Exporter] Module initialized.\n"
)
