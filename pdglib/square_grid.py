# encoding: utf-8

import gvsig
from gvsig import geom
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory

def pointDensityGrid_square(self, lado, store, output, addEmptyGrids, projection, envelope, filterExpression):
  deltaX= lado*0.2
  deltaY= lado*0.2
  print "pointDensityGrid_square"
  ###
  ### Selection
  ###
  if store.getSelection().getSize()==0:
    if filterExpression!='':
      featuresLayer = store.getFeatureSet(filterExpression)
    else:
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
  
  sef = SpatialEvaluatorsFactory.getInstance()
  
  fq = store.createFeatureQuery()
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
      #contar los puntos dentro de cada rejilla
      #evaluator = sef.intersects(square, projection, store)
      #TODO: Try to use selection
      featureType = store.getDefaultFeatureType()
      geomName = featureType.getDefaultGeometryAttributeName()
      builder = store.createExpressionBuilder()
      evaluator = sef.intersects(square, projection, featureType,geomName,builder)
      fq.setFilter(evaluator)

      if store.getSelection().getSize()==0:
        fs = store.getFeatureSet(fq)
      else:
        fs = store.getSelection()
    
      #fs = store.getFeatureSet(fq)
      #allParams = getInitAllParams(store)
      count = 0
      for k in fs:
          if k.getDefaultGeometry().intersects(square):
              count += 1
              #getAllValuesForExpression(allParams)
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
  
  
  