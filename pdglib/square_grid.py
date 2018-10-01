# encoding: utf-8

import gvsig
from gvsig import geom
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory

def pointDensityGrid_square(self, lado, store, output, addEmptyGrids, projection):
  deltaX=lado*0.2
  deltaY=lado*0.2


  if store.getSelection().getSize()==0:
    featuresLayer = store.getFeatures()
  else:
    featuresLayer = store.getSelection()
    print "SELECTION", featuresLayer, type(featuresLayer)

  #TODO Adjust grid to selection
  envelope=store.getEnvelope()
  infX = envelope.getLowerCorner().getX()-deltaX
  infY = envelope.getLowerCorner().getY()-deltaY
  supX = envelope.getUpperCorner().getX()+deltaX
  supY = envelope.getUpperCorner().getY()+deltaY

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
      count = 0
      for k in fs:
          if k.getDefaultGeometry().intersects(square):
              count += 1
      if addEmptyGrids==False and count==0:
        continue
      newFeature = output.createNewFeature()
      newFeature["ID"]=id_
      newFeature["GEOMETRY"]=square
      newFeature["COUNT"]=count
      value = 0

      newFeature["VALUE"]=value
      output.insert(newFeature)
      id_+=1
