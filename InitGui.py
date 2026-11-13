# -*- coding: utf-8 -*-
"""GUI registration for the FreeCAD PrusaSlicer Exporter workbench.

FreeCAD may execute InitGui.py without __file__ and with isolated scopes.
Avoid references to module-level variables inside the workbench class.
"""

import FreeCAD as App
import FreeCADGui as Gui


class PrusaSlicerExporterWorkbench(Gui.Workbench):
    MenuText = "PrusaSlicer Exporter"
    ToolTip = "Send selected parts and faces to PrusaSlicer"

    # Evaluate inside class scope: FreeCAD may not expose module globals.
    Icon = App.getUserAppDataDir() + "Mod/FreeCAD-PrusaSlicer-Exporter/Resources/icons/PrusaExporter.svg"

    def Initialize(self):
        import os
        import sys

        addon_path = os.path.join(
            App.getUserAppDataDir(), "Mod", "FreeCAD-PrusaSlicer-Exporter"
        )
        if addon_path not in sys.path:
            sys.path.insert(0, addon_path)

        import PrusaExporter

        Gui.addCommand("PrusaExporter_Send", PrusaExporter.SendCommand())
        self.appendToolbar("PrusaSlicer", ["PrusaExporter_Send"])
        self.appendMenu("PrusaSlicer", ["PrusaExporter_Send"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(PrusaSlicerExporterWorkbench())
