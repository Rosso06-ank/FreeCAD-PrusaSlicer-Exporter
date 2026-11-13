import FreeCAD as App
import FreeCADGui as Gui
import os

class PrusaSlicerExporterWorkbench(Gui.Workbench):
    MenuText = 'PrusaSlicer Exporter'
    ToolTip = 'Send selected faces or solids to PrusaSlicer'
    Icon = os.path.join(os.path.dirname(__file__), 'Resources', 'icons', 'PrusaExporter.svg')

    def Initialize(self):
        import PrusaExporter
        Gui.addCommand('PrusaExporter_Send', PrusaExporter.SendCommand())
        self.appendToolbar('PrusaSlicer', ['PrusaExporter_Send'])
        self.appendMenu('PrusaSlicer', ['PrusaExporter_Send'])

    def GetClassName(self):
        return 'Gui::PythonWorkbench'

Gui.addWorkbench(PrusaSlicerExporterWorkbench())

