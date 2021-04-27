# collection of methods converting from ifcopenshell to shapely

from shapely.geometry import Point, Polygon

def to_point(ifc_point):
    return Point(ifc_point.Coordinates)

# def to_polygon(profile):
#     if not profile.is_a('IfcProfileDef'):
#         raise ValueError('Value not of type "IfcProfileDef"')
