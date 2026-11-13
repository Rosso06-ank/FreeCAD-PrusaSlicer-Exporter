# -*- coding: utf-8 -*-

import FreeCAD as App
import FreeCADGui as Gui
import os

# FreeCAD modül klasörünü bul
ADDON_PATH = os.path.join(
    App.getUserAppDataDir(),
    "Mod",
    "FreeCAD-PrusaSlicer-Exporter"
)

ICON_PATH = os.path.join(
    ADDON_PATH,
    "Resources",
    "icons",
    "PrusaExporter.svg"
)


class PrusaSlicerExporterWorkbench(Gui.Workbench):

    MenuText = "PrusaSlicer Exporter"

    ToolTip = "Send selected parts and faces to PrusaSlicer"

    Icon = ICON_PATH

    def Initialize(self):
        import sys

        if ADDON_PATH not in sys.path:
            sys.path.insert(0, ADDON_PATH)

        import PrusaExporter

        Gui.addCommand(
            "PrusaExporter_Send",
            PrusaExporter.SendCommand()
        )

        self.appendToolbar(
            "PrusaSlicer",
            ["PrusaExporter_Send"]
        )

        self.appendMenu(
            "PrusaSlicer",
            ["PrusaExporter_Send"]
        )

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(PrusaSlicerExporterWorkbench())

App.Console.PrintMessage(
    "[PrusaSlicer Exporter] Workbench registered.\n"
)
