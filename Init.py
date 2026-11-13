import FreeCAD
import FreeCADGui as Gui
import os
import sys
import traceback

addon = os.path.join(
    FreeCAD.getUserAppDataDir(),
    "Mod",
    "FreeCAD-PrusaSlicer-Exporter"
)

if addon not in sys.path:
    sys.path.insert(0, addon)

try:
    initgui = os.path.join(addon, "InitGui.py")

    with open(initgui, encoding="utf-8") as f:
        code = compile(f.read(), initgui, "exec")

    exec(code, {
        "__file__": initgui,
        "__name__": "__main__"
    })

    print("Workbench başarıyla yüklendi!")

except Exception:
    traceback.print_exc()

print([
    name for name in Gui.listWorkbenches()
    if "Prusa" in name
])
