# encoding: utf-8

import gvsig
from gvsig import geom
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from hexa_grid import getFeatureSetForGeoprocess

def pointDensityGrid_square(self, lado, store, output, addEmptyGrids, projection, envelope, filterExpression, geomFieldName):
  deltaX= lado*0.2
  deltaY= lado*0.2
  ###
  ### Selection
  ###
  if store.getSelection().getSize()==0:
    featuresLayer = store.getFeatureSet()
  else:
    featuresLayer = store.getSelection()
  totalSize = float(featuresLayer.getSize())
  #TODO Adjust grid to selection

  ###
  ### ENVELOPE
  ###
  #env = self.getAnalysisExtent().getAsJTSGeometry().getEnvelopeInternal()
  if envelope==None:
    envelope=store.getEnvelope()

  infX = envelope.getMinX()-deltaX
  infY = envelope.getMinY()-deltaY
  supX = envelope.getMaxX()+deltaX
  supY = envelope.getMaxY()+deltaY

  dX = supX - infX
  dY = supY - infY
  
  id_=0

  increY = lado
  increX = lado
  #pdb.set_trace()
  numero_filas=dY/lado
  numero_columnas=dX/lado
  
  self.setRangeOfValues(0,int(numero_filas*numero_columnas))
  self.setProgressText("Processing " + str(int(numero_filas*numero_columnas)) + " features")
  n = 0
  #expandedFeatureType = createGroupyByFeatureType(store)

  for i in range(0, int(numero_columnas)+1):
    for j in range(0, int(numero_filas)+1):
      if self.isCanceled():
        break
      else:
        self.setCurValue(n)
        n+=1
        self.setProgressText("Processing "+str(n)+" in "+str(int(numero_filas*numero_columnas))+" features")
      cX = infX + increX*i #2*increX*i
      cY = infY + increY*j #1.5*lado*j
      p1 = geom.createPoint(geom.D2, cX, cY)
      p2 = geom.createPoint(geom.D2, cX+increX, cY)
      p3 = geom.createPoint(geom.D2, cX+increX, cY+increY)
      p4 = geom.createPoint(geom.D2, cX, cY+increY)
      square = geom.createPolygon(vertexes=[p1,p2,p3,p4,p1])
      square.setProjection(projection)
      
      fs = getFeatureSetForGeoprocess(store, filterExpression, square, geomFieldName)

      count = fs.getSize()

      if addEmptyGrids==False and count==0:
        continue
      newFeature = output.createNewFeature()
      newFeature["ID"]=id_
      newFeature["GEOMETRY"]=square
      newFeature["COUNT"]=count
      newFeature["PERC"]= (count/totalSize)*100
      newFeature["TOTAL"]=totalSize
      #value = 0
      #newFeature["VALUE"]=value
      output.insert(newFeature)
      id_+=1

def main(*args):
  layer = gvsig.currentLayer().getFeatureStore()
  allParams = {}
  store = layer.getFeatureStore()
  ft = createGroupyByFeatureType(store)
  print "Final: ", ft

def createGroupyByFeatureType(store):
  ft = store.getDefaultFeatureType()
  newft = gvsig.createFeatureType(ft)
  for attr in ft.getAttributeDescriptors():
    dataTypeName = attr.getDataTypeName()
    name = attr.getName()
    size = attr.getSize()+5
    if dataTypeName=="String":
      pass
    elif dataTypeName=="Double" or dataTypeName=="Long":
      appendNumericField(name, "Double", size, newft)
    elif dataTypeName=="Integer":
      appendNumericField(name, dataTypeName, size, newft)
    elif dataTypeName=="Date":
      pass
    elif dataTypeName=="GEOMETRY":
      pass
    else:
      print "Not supported: ", dataTypeName
    print dataTypeName
    name = attr.getName()
    typefield = attr.getType()
  return newft

def appendNumericField(name, dataTypeName, size, newft):
  prefix = ["S","F","A","X","N"]
  print "name:", name
  if len(name)==10:
    name = name[:-1]
  for p in prefix:
    newName = p+name
    print "newName:", newName
    newft.append(newName, dataTypeName, size)
  
def setInitAllParams(store):
  allParams = {}
  ft = store.getDefaultFeatureType()
  for attr in ft.getAttributeDescriptors():
    name = attr.getName()
    typefield = attr.getType()
    allParams[name] = 0
    print name,typefield
  
  
  