import csv
import bpy

def write_some_data(context, filepath, use_some_setting):
    print("running write_some_data...")
    f = open(filepath, 'w', encoding='utf-8')
    f.write("Hello World %s" % use_some_setting)
    f.close()

    return {'FINISHED'}


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

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(DreamteckSplineExporter.bl_idname, text="Text Export Operator")


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
#header = ['PositionX','PositionY','PositionZ','TangentX','TangentY','TangentZ','Tangent2X','Tangent2Y','Tangent2Z','NormalX','NormalY','NormalZ','Size','ColorR','ColorG','ColorB','ColorA']
#rotate 90 degrees on X axis 
#can get rid of normals property
header = ['PositionX','PositionY','PositionZ','TangentX','TangentY','TangentZ','Tangent2X','Tangent2Y','Tangent2Z','Size','ColorR','ColorG','ColorB','ColorA']

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
data = []
for point in bpy.context.selected_objects[0].data.splines[0].bezier_points:
    data.append([
        point.co.x, point.co.z, point.co.y, #swizzle
        point.handle_right.x, point.handle_right.z, point.handle_right.y,  #swizzle
        point.handle_left.x, point.handle_left.z, point.handle_left.y, #swizzle
        #0.0, 1.0, 0.0,
        point.radius,
        1.0, 1.0, 1.0, 1.0
        ])

with open(filepath, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)


