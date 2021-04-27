# collection of methods converting from shapely to ifcopenshell

def add_point(ifc_model,point):
    if isinstance(point, tuple):
        return ifc_model.createIfcCartesianPoint(point)
    else:
        if point.has_z:
            point = (point.x,point.y,point.z)
        else:
            point = (point.x,point.y)
        return ifc_model.createIfcCartesianPoint(point)

def add_polyline(ifc_model,polyline):    
    exterior_points = tuple(map(lambda x: add_point(ifc_model, x),polyline.coords))
    return ifc_model.createIfcPolyline(exterior_points)

def add_polygon(ifc_model,shapely_polygon,profile_type='AREA'):
    outercurve = add_polyline(ifc_model,shapely_polygon.exterior)
    if shapely_polygon.interiors:
        if profile_type != 'AREA':
            raise ValueError("WR1: The type of the profile shall be AREA, as it can only be involved in the definition of a swept area.")
        innercurves = tuple(map(lambda x: add_polyline(ifc_model,x),shapely_polygon.interiors))
        return ifc_model.createIfcArbitraryProfileDefWithVoids(profile_type,OuterCurve=outercurve, InnerCurves=innercurves)
    else:
        return ifc_model.createIfcArbitraryClosedProfileDef(profile_type,OuterCurve=outercurve)

def polygon_to_ifcextrudedareasolid(ifc_model,shapely_polygon,position=None,extrudeddirection=None,depth=0.1):
    if not position:
        point = ifc_model.createIfcCartesianPoint((0.,0.,0.))
        d1 = ifc_model.createIfcDirection((0.,0.,1.))
        d2 = ifc_model.createIfcDirection((1.,0.,0.))
        position = ifc_model.createIfcAxis2Placement3D(point,d1,d2)
    if not extrudeddirection:
        extrudeddirection = ifc_model.createIfcDirection((0.,0.,1.))
    swept_area = add_polygon(ifc_model,shapely_polygon)
    return ifc_model.createIfcExtrudedAreaSolid(swept_area,position,extrudeddirection,depth)

def polygon_to_sweptsolid(ifc_model,context,shapely_polygon,position=None,extrudeddirection=None,depth=0.1):
    if shapely_polygon.geom_type == 'Polygon':
        shapely_polygon = [shapely_polygon]
    items = [ polygon_to_ifcextrudedareasolid(ifc_model,polygon,position,extrudeddirection,depth) for polygon in shapely_polygon ]
    return ifc_model.createIfcShapeRepresentation(context, "Body", "SweptSolid", items)

# def polygon_to_productdefinitionshape(ifc_model,context,shapely_polygon,position=None,extrudeddirection=None,depth=0.1):
#     representations = [polygon_to_sweptsolid(ifc_model,context,shapely_polygon,position=position,extrudeddirection=extrudeddirection,depth=depth)]
#     return ifc_model.createIfcProductDefinitionShape(None, None, representations)

# def polygon_to_ifcslab(ifc_model,shapely_polygon,owner_history,context,guid,name=None,description=None,position=None,extrudeddirection=None,depth=0.1):
#     representation = polygon_to_productdefinitionshape(ifc_model,context,shapely_polygon,position=None,extrudeddirection=extrudeddirection,depth=depth)
#     return ifc_model.createIfcSlab(guid, owner_history, Name=name, Description=description, ObjectType=None, ObjectPlacement=position, Representation=representation, Tag=None,PredefinedType='NOTDEFINED')
