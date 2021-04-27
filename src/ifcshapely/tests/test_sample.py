import ifcopenshell
import shapely.wkt

from from_shapely import *
    
def test_add_point():
    ifc_model = ifcopenshell.file(None)
    shapely_point = shapely.wkt.loads('POINT (30 10 50)')
    assert add_point(ifc_model,shapely_point).is_a('IfcCartesianPoint')
    
def test_add_polyline():
    ifc_model = ifcopenshell.file(None)
    shapely_polygon = shapely.wkt.loads('POLYGON ((51.0 3.0, 51.3 3.61, 51.3 3.0, 51.0 3.0))')
    assert add_polygon(ifc_model,shapely_polygon).is_a('IfcProfileDef')
    
def test_add_polyline_with_holes():
    ifc_model = ifcopenshell.file(None)
    shapely_polygon = shapely.wkt.loads('POLYGON ((51.0 3.0, 51.3 3.61, 51.3 3.0, 51.0 3.0),(51.1 3.1, 51.2 3.1, 51.3 3.2,51.1 3.1))')
    assert add_polygon(ifc_model,shapely_polygon).is_a('IfcArbitraryProfileDefWithVoids')