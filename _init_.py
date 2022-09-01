import csv
from queue import Empty
from select import select
from traceback import print_exception
import bpy

bl_info = {
    "name" : "DreamteckSplineExporter",
    "author" : "Holly Newlands",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

def write_csv(context, filepath, header, data):
    print("running write_some_data...")
    with open(filepath, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write multiple rows
        writer.writerows(data)
    return {'FINISHED'}

def valid_selection():
    if len(bpy.context.selected_objects) < 1:
        return False
    if len(bpy.context.selected_objects[0].data.splines) < 1:
        return False
    return True

def get_bezier_from_selection():
    return bpy.context.selected_objects[0].data.splines[0]

def convert_bezier_to_csv(spline):
    data = []
    for point in spline.bezier_points:
        data.append([
            point.co.x, point.co.z, point.co.y, #swizzle
            point.handle_right.x, point.handle_right.z, point.handle_right.y,  #swizzle
            point.handle_left.x, point.handle_left.z, point.handle_left.y, #swizzle
            #0.0, 1.0, 0.0, #TODO: Blender splines don't have a normal property, only a twist value
            point.radius,
            1.0, 1.0, 1.0, 1.0
            ])
    return data

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class DreamteckSplineExporter(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Some Data"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"
    #full_header = ['PositionX','PositionY','PositionZ','TangentX','TangentY','TangentZ','Tangent2X','Tangent2Y','Tangent2Z','NormalX','NormalY','NormalZ','Size','ColorR','ColorG','ColorB','ColorA']
    csv_header = ['PositionX','PositionY','PositionZ','TangentX','TangentY','TangentZ','Tangent2X','Tangent2Y','Tangent2Z','Size','ColorR','ColorG','ColorB','ColorA']
    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        if valid_selection():
            selection = get_bezier_from_selection()
            csv_data = convert_bezier_to_csv(selection)
            return write_csv(context, self.filepath, self.csv_header, csv_data)
        else:
            self.report({'WARNING'}, "There was no bezier curve in selection to export.")
            return {'FINISHED'}


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(DreamteckSplineExporter.bl_idname, text="Export Dreamteck Spline (.csv)")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(DreamteckSplineExporter)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(DreamteckSplineExporter)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')

filepath = r"spline_export.csv"
#rotate 90 degrees on X axis 
#can get rid of normals property

#https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13
#bpy.context.selected_objects[0].data.splines[0].bezier_points
#bpy.context.selected_objects[0].data.splines[0].bezier_points[0].radius
#https://blender.stackexchange.com/questions/258052/select-end-points-of-a-curve-using-blender-scripting
#co -- coordinate
#tangentxyz --> handle left
#tangent2xyz --> handle right
#radius --> size
#no color
#no normal (maybe cross tangent w/ forward? or just dont export





