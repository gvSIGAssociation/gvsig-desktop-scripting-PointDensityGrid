# encoding: utf-8

import gvsig
from gvsig import geom
from gvsig.libs.toolbox import ToolboxProcess, NUMERICAL_VALUE_DOUBLE,SHAPE_TYPE_POLYGON,NUMERICAL_VALUE_INTEGER,SHAPE_TYPE_POLYGON, SHAPE_TYPE_POINT
from addons.PointDensityGrid.pdglib.hexa_grid import pointDensityGrid_hexa
from addons.PointDensityGrid.pdglib.square_grid import pointDensityGrid_square

GRID_HEXAGON_HORIZONTAL = "Grid hexagon horizontal"
GRID_HEXAGON_VERTICAL = "Grid hexagon vertical"
GRID_SQUARE = "Grid square"


def main(*args):

  sextantelayer = gvsig.currentLayer()
  distancegrid = 0.1
  gridType = GRID_HEXAGON_HORIZONTAL
  addEmptyGrids = True
  valueExpression = ""

  store = sextantelayer.getFeatureStore()
  projection = sextantelayer.getProjection()
  pointDensityGridCreation(None, store, gridType, distancegrid, addEmptyGrids, projection)

def pointDensityGridCreation(self, store, gridType, distancegrid, addEmptyGrids, projection, envelope):
  #features = store.features()

  newSchema = gvsig.createFeatureType()
  newSchema.append("ID", "INTEGER", 10)
  newSchema.append("COUNT", "INTEGER", 20)
  newSchema.append("TOTAL", "INTEGER", 20)
  #newSchema.append("VALUE", "DOUBLE", 20)
  newSchema.append("PERC", "DOUBLE", 5)
  newSchema.append("GEOMETRY", "GEOMETRY")
  newSchema.get("GEOMETRY").setGeometryType(geom.POLYGON, geom.D2)
  ### Capa 2: Aprovechando las opciones de la Toolbox
  
  output_store = self.buildOutPutStore(
          newSchema,
          SHAPE_TYPE_POLYGON,
          "DensityGrid",
          "RESULT_POLYGON"
  )

  #pdb.set_trace()
  n = 0

  if gridType==GRID_HEXAGON_HORIZONTAL:
    rotate = False
    pointDensityGrid_hexa(self, distancegrid, store, output_store, rotate, addEmptyGrids, projection, envelope)
  elif gridType==GRID_HEXAGON_VERTICAL:
    rotate = True
    pointDensityGrid_hexa(self, distancegrid, store, output_store, rotate, addEmptyGrids, projection, envelope)
  elif gridType==GRID_SQUARE:
    #pointDensityGrid_square(distancegrid,distancegrid,store)
    pointDensityGrid_square(self, distancegrid, store, output_store, addEmptyGrids, projection, envelope)
  output_store.finishEditing()