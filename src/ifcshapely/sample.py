import uuid

import ifcopenshell
import ifcopenshell.geom
import shapely.wkt

from from_shapely import *
from to_shapely import *
    
if __name__ == '__main__':
    ifc_model = ifcopenshell.file(None)

    shapely_point = shapely.wkt.loads('POINT (30 10 50)')
    ifc_point = add_point(ifc_model,shapely_point)
    print(f"IFC point: {ifc_point}")

    shapely_polygon = shapely.wkt.loads('POLYGON ((51.0 3.0, 51.3 3.61, 51.3 3.0, 51.0 3.0))')
    ifc_polygon = add_polygon(ifc_model,shapely_polygon)
    print(f"IFC polygon: {ifc_polygon}")

    extrusion = polygon_to_ifcextrudedareasolid(ifc_model,shapely_polygon)
    print(f"IFC extruded polygon: {extrusion}")

    # guid=ifcopenshell.guid.compress(uuid.uuid1().hex)
    # owner_history = ifc_model.createIfcOwnerHistory()
    # context = ifc_model.createIfcGeometricRepresentationContext()
    # slab = polygon_to_ifcslab(ifc_model,shapely_polygon,owner_history,context,guid)
    # print(slab)

    shapely_point_roundtrip = point_to_shapely(ifc_point)
    print(f"Shapely point: {shapely_point_roundtrip}")

    ifc_model.write("sample.ifc")