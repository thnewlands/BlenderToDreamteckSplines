import csv
import bpy

filepath = r"spline_export.csv"
#header = ['PositionX','PositionY','PositionZ','TangentX','TangentY','TangentZ','Tangent2X','Tangent2Y','Tangent2Z','NormalX','NormalY','NormalZ','Size','ColorR','ColorG','ColorB','ColorA']
#rotate 90 degrees on X axis 
#can get rid of normals property
header = ['PositionX','PositionY','PositionZ','TangentX','TangentY','TangentZ','Tangent2X','Tangent2Y','Tangent2Z','Size','ColorR','ColorG','ColorB','ColorA']
data = [
]
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


