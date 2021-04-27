import uuid

from ... import ifcopenshell

# import ifcopenshell
# import ifcopenshell.geom

import shapely.wkt
from shapely.geometry import Point
    
if __name__ == '__main__':
    ifc_model = ifcopenshell.file(None)

    shapely_point = shapely.wkt.loads('POINT (30 10 50)')
    ifc_point = point_to_ifc(ifc_model,shapely_point)
    print(ifc_point)

    # shapely_point2 = point_to_shapely(ifc_point)
    # print(shapely_point2)

    shapely_polygon = shapely.wkt.loads('POLYGON ((51.0 3.0, 51.3 3.61, 51.3 3.0, 51.0 3.0))')

    ifc_polygon = polygon_to_ifc(ifc_model,shapely_polygon)
    print(f"IFC Polygon: {ifc_polygon}")

    extrusion = polygon_to_ifcextrudedareasolid(ifc_model,shapely_polygon)
    print(extrusion)

    guid=ifcopenshell.guid.compress(uuid.uuid1().hex)
    owner_history = ifc_model.createIfcOwnerHistory()
    print(owner_history)
    context = ifc_model.createIfcGeometricRepresentationContext()
    print(context)

    slab = polygon_to_ifcslab(ifc_model,shapely_polygon,owner_history,context,guid)
    print(slab)


    ifc_model.write("demo.ifc")
    
    # settings = ifcopenshell.geom.settings()
    # settings.set(settings.USE_WORLD_COORDS, False)
    # ifc_model = ifcopenshell.open('../../308/D_T_REG_A_3dBAG.ifc')
    # for product in ifc_model.by_type('IfcProduct'):
    #     try:
    #         tessellated_shape = ifcopenshell.geom.create_shape(settings, product)
    #         print(tessellated_shape.geometry)
    #         print(type(tessellated_shape.geometry))
    #     except:
    #         print("no")