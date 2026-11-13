"""Export selected FreeCAD faces/bodies as STL and launch PrusaSlicer."""
import os
import re
import shutil
import subprocess
import tempfile
import traceback

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Mesh
import MeshPart

# Editable defaults; face thickness 0 produces an open, non-printable surface.
FACE_THICKNESS_MM = 0.0
LINEAR_DEFLECTION_MM = 0.10
ANGULAR_DEFLECTION_RAD = 0.35
SLICER_PATH = ''  # Optional absolute path, e.g. /usr/bin/prusa-slicer


def log(message):
    App.Console.PrintMessage('[PrusaExporter] ' + str(message) + '\n')


def valid_shape(obj):
    try:
        return hasattr(obj, 'Shape') and not obj.Shape.isNull() and bool(obj.Shape.Faces)
    except Exception:
        return False


def parent_body(obj):
    if obj.TypeId == 'PartDesign::Body':
        return obj
    try:
        parent = obj.getParentGeoFeatureGroup()
        if parent and parent.TypeId == 'PartDesign::Body':
            return parent
    except Exception:
        pass
    return obj


def face_to_shape(face):
    if FACE_THICKNESS_MM <= 0:
        return face.copy()
    if not isinstance(face.Surface, Part.Plane):
        raise ValueError('Thickness export only supports planar faces.')
    normal = face.normalAt(0, 0)
    return face.extrude(normal.multiply(FACE_THICKNESS_MM))


def get_shapes(doc):
    shapes, names, seen = [], [], set()
    selected = Gui.Selection.getSelectionEx()
    if selected:
        for entry in selected:
            obj = entry.Object
            face_names = [n for n in entry.SubElementNames if re.fullmatch(r'Face\d+', n)]
            if face_names:
                for name in face_names:
                    key = (obj.Name, name)
                    if key in seen:
                        continue
                    face = obj.getSubObject(name)
                    if face is None or face.isNull() or face.ShapeType != 'Face':
                        raise ValueError('Cannot resolve face: %s.%s' % (obj.Label, name))
                    shapes.append(face_to_shape(face))
                    names.append('%s.%s' % (obj.Label, name))
                    seen.add(key)
            else:
                target = parent_body(obj)
                if valid_shape(target) and target.Name not in seen:
                    shapes.append(target.Shape.copy())
                    names.append(target.Label)
                    seen.add(target.Name)
    else:
        visible = [o for o in doc.Objects if valid_shape(o) and o.ViewObject and o.ViewObject.Visibility]
        for obj in visible:
            parent = parent_body(obj)
            if parent is not obj and parent in visible:
                continue
            if obj.Name not in seen:
                shapes.append(obj.Shape.copy())
                names.append(obj.Label)
                seen.add(obj.Name)
    return shapes, names


def slicer_command():
    if SLICER_PATH:
        if not os.path.isfile(SLICER_PATH):
            raise RuntimeError('PrusaSlicer not found: ' + SLICER_PATH)
        return SLICER_PATH
    exe = shutil.which('prusa-slicer') or shutil.which('PrusaSlicer')
    if not exe:
        raise RuntimeError('PrusaSlicer not found in PATH. Set SLICER_PATH in PrusaExporter.py.')
    return exe


def export_to_slicer():
    doc = App.ActiveDocument
    if doc is None:
        raise RuntimeError('Open a FreeCAD document first.')
    doc.recompute()
    shapes, names = get_shapes(doc)
    if not shapes:
        raise RuntimeError('Select a face or object, or make a solid visible.')
    result = Mesh.Mesh()
    for shape in shapes:
        mesh = MeshPart.meshFromShape(Shape=shape,
                                      LinearDeflection=LINEAR_DEFLECTION_MM,
                                      AngularDeflection=ANGULAR_DEFLECTION_RAD,
                                      Relative=False)
        if mesh.CountFacets:
            result.addMesh(mesh)
    if not result.CountFacets:
        raise RuntimeError('No STL triangles generated.')
    folder = tempfile.mkdtemp(prefix='freecad_prusaslicer_')
    filename = re.sub(r'[^a-zA-Z0-9_.-]+', '_', doc.Label).strip('._') or 'freecad'
    path = os.path.join(folder, filename + '.stl')
    result.write(path)
    log('Exported: ' + ', '.join(names))
    log('STL: ' + path)
    subprocess.Popen([slicer_command(), '--single-instance', path],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)
    if FACE_THICKNESS_MM == 0 and any('.Face' in n for n in names):
        log('Warning: a zero-thickness face STL is not a printable solid.')
    log('Sent to PrusaSlicer (reuse of window depends on PrusaSlicer preferences).')


class SendCommand:
    def GetResources(self):
        return {
            'Pixmap': os.path.join(os.path.dirname(__file__), 'Resources', 'icons', 'PrusaExporter.svg'),
            'MenuText': 'Send to PrusaSlicer',
            'ToolTip': 'Export selected faces or solids to PrusaSlicer (no save needed)'
        }

    def Activated(self):
        try:
            export_to_slicer()
        except Exception as exc:
            App.Console.PrintError('[PrusaExporter] ' + str(exc) + '\n')
            App.Console.PrintError(traceback.format_exc() + '\n')

    def IsActive(self):
        return App.ActiveDocument is not None

