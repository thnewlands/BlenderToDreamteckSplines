import csv
from queue import Empty
from select import select
from traceback import print_exception
import bpy

bl_info = {
    "name" : "Spline Exporter for Dreamteck Splines",
    "author" : "Holly Newlands",
    "description" : "Export bezier curves as csv files for import in the DreamTeck Splines plugin for Unity.",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Import-Export"
}

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator

class DreamteckSplineExporter(Operator, ExportHelper):
    """Export bezier curves as csv files for import in the DreamTeck Splines plugin for Unity."""
    bl_idname = "spline_exporter.bezier_curve"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export bezier curve to Dreamteck Splines"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"
    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    #['PositionX','PositionY','PositionZ','TangentX','TangentY','TangentZ','Tangent2X','Tangent2Y','Tangent2Z','NormalX','NormalY','NormalZ','Size','ColorR','ColorG','ColorB','ColorA']
    #TODO: This could be a property group
    use_position: BoolProperty(
        name="Use Position",
        description="Write positions of bezier curve.",
        default=True,
    )
    use_tangent: BoolProperty(
        name="Use Tangent",
        description="Write left tangents of bezier curve.",
        default=True,
    )
    use_tangent2: BoolProperty(
        name="Use Tangent2",
        description="Write right tangents of bezier curve.",
        default=True,
    )
    use_normal: BoolProperty(
        name="Use Normal",
        description="NOTE: Sets all normals to (0,1,0) until I find a better process. Currently here as placeholder.",
        default=True,
    )
    use_size: BoolProperty(
        name="Use Size",
        description="Write sizes of bezier curve points.",
        default=True,
    )
    use_color: BoolProperty(
        name="Use Color",
        description="NOTE: Sets all colors to (1,1,1,1) until I find a better process. Currently here as placeholder.",
        default=True,
    )

    def get_header(self):
        header = []
        if self.use_position:
            header += ['PositionX','PositionY','PositionZ']
        if self.use_tangent:
            header += ['TangentX','TangentY','TangentZ']
        if self.use_tangent2:
            header += ['Tangent2X','Tangent2Y','Tangent2Z']
        if self.use_normal:
            header += ['NormalX','NormalY','NormalZ']
        if self.use_size:
            header += ['Size']
        if self.use_color:
            header += ['ColorR','ColorG','ColorB', 'ColorA']
        return header

    def convert_bezier_to_csv(self, spline):
        data = []
        for point in spline.bezier_points:
            values = []
            if self.use_position:
                #Position -- co (local coordinate?)
                values += [point.co.x, point.co.z, point.co.y]
            if self.use_tangent:
                #TangentXYZ --> handle_left
                values += [point.handle_right.x, point.handle_right.z, point.handle_right.y]
            if self.use_tangent2:
                #Tangent2XYZ --> handle_right
                values += [point.handle_left.x, point.handle_left.z, point.handle_left.y]
            if self.use_normal:
                #NormalXYZ --> !! not defined in blender !! 
                values += [0.0, 1.0, 0.0] #TODO: Blender splines don't have a normal property, only a twist value
            if self.use_size:
                #Size --> radius
                values += [point.radius]
            if self.use_color:
                #ColorRGB --> !! not defined in blender !!
                values += [1.0, 1.0, 1.0, 1.0] #blender doesn't define color so just default to white 
            data.append(values)
        return data
    
    def validate_selection(self):
        if len(bpy.context.selected_objects) < 1:
            return False
        if len(bpy.context.selected_objects[0].data.splines) < 1:
            return False
        return True

    def get_bezier_from_selection(self):
        return bpy.context.selected_objects[0].data.splines[0]

    def write_csv(self, context, filepath, header, data):
        print("writing csv...")
        with open(filepath, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            # write multiple rows
            writer.writerows(data)
        print("Successfully exported curve to " + filepath)
        return {'FINISHED'}
        
    def execute(self, context):
        if self.validate_selection():
            selection = self.get_bezier_from_selection()
            csv_data = self.convert_bezier_to_csv(selection)
            return self.write_csv(context, self.filepath, self.get_header(), csv_data)
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
