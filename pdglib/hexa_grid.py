# encoding: utf-8

import gvsig
from gvsig import geom
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from org.gvsig.fmap.dal import DALLocator
from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
from gvsig import logger
from gvsig import LOGGER_INFO
import time

def getFeatureSetForGeoprocess(store, filterExpression, spatialGeometry=None, geomFieldName="GEOMETRY"):
  if filterExpression==None: #.getPhrase()=="": #org.gvsig.expressionevaluator.Expression
    if store.getSelection().getSize()==0:
      builder = ExpressionEvaluatorLocator.getManager().createExpressionBuilder()
      expr1 = builder.ST_Intersects(
            builder.geometry(spatialGeometry),
            builder.column(geomFieldName)
          ).toString()
      
      #cloneExpression = filterExpression.clone()
      cloneExpression = ExpressionEvaluatorLocator.getManager().createExpression()
      cloneExpression.setPhrase(expr1)
      evaluator = DALLocator.getDataManager().createFilter(cloneExpression)
      """
      exp = ExpressionEvaluatorLocator.getManager().createExpression()
      exp.setPhrase(expr1)
      evaluator = DALLocator.getDataManager().createExpresion(exp)
      """
      fq = store.createFeatureQuery()
      fq.addFilter(evaluator)
      #fq.retrievesAllAttributes()
      #fq.addAttributeName("Id")
      featuresLayer = store.getFeatureSet(fq)
      return featuresLayer
    else:
      featuresLayer = store.getSelection()
      return featuresLayer
  else:
    builder = ExpressionEvaluatorLocator.getManager().createExpressionBuilder()
    expr2 = builder.and(
        builder.custom(filterExpression.getPhrase()),
        builder.ST_Intersects(
          builder.geometry(spatialGeometry),
          builder.column("GEOMETRY")
        )
    ).toString()
    #logger("Expression 2:"+expr2, LOGGER_INFO)
    cloneExpression = filterExpression.clone()
    cloneExpression.setPhrase(expr2)
    evaluator = DALLocator.getDataManager().createFilter(cloneExpression)
    fq = store.createFeatureQuery()
    fq.addFilter(evaluator)
    #fq.retrievesAllAttributes()
    featuresLayer = store.getFeatureSet(fq)
    return featuresLayer
  
def pointDensityGrid_hexa(self, lado, store, output, rotate, addEmptyGrids, projection, envelope, filterExpression, geomName):
  deltaX=lado*0.0000001
  deltaY=lado*0.0000001
  if store.getSelection().getSize()==0:
    featuresLayer = store.getFeatureSet()
  else:
    featuresLayer = store.getSelection()
  totalSize = float(featuresLayer.getSize())
  if envelope==None:
      envelope=store.getEnvelope()
  #infX = envelope.getLowerCorner().getX()-deltaX
  #infY = envelope.getLowerCorner().getY()-deltaY
  #supX = envelope.getUpperCorner().getX()+deltaX
  #supY = envelope.getUpperCorner().getY()+deltaY
  infX = envelope.getMinX()-deltaX
  infY = envelope.getMinY()-deltaY
  supX = envelope.getMaxX()+deltaX
  supY = envelope.getMaxY()+deltaY
  
  dX = supX - infX
  dY = supY - infY
  
  id_=0
  n = 0
  #sef = SpatialEvaluatorsFactory.getInstance()
  fq = store.createFeatureQuery()

  if rotate: #
    start = time.time()
    #print "Time..: ", start - time.time()
    increY = lado*0.5
    increX = (pow((pow(lado,2)-pow(lado*0.5,2)),0.5))
    numero_filas=int(dY/(lado*1.5))+2
    numero_columnas=int(dX/(increX*2))+2
    self.setRangeOfValues(0,int(numero_filas*numero_columnas))
    for i in range(0, numero_columnas):
      for j in range(0, numero_filas):
        if self.isCanceled():
          break
        else:
          self.setCurValue(n)
          n+=1
          self.setProgressText("Processing "+str(n)+" in "+str(int(numero_filas*numero_columnas))+" features")
        cX = infX + 2*increX*i
        cY = infY + 1.5*lado*j
        if j%2!=0:
          cX=cX-increX
        p1 = geom.createPoint(geom.D2, cX-increX, cY-increY)
        p2 = geom.createPoint(geom.D2, cX-increX, cY+increY)
        p3 = geom.createPoint(geom.D2, cX, cY+lado)
        p4 = geom.createPoint(geom.D2, cX+increX, cY+increY)
        p5 = geom.createPoint(geom.D2, cX+increX, cY-increY)
        p6 = geom.createPoint(geom.D2, cX, cY-lado)
        hexa = geom.createPolygon(vertexes=[p1,p2,p3,p4,p5,p6,p1])
        hexa.setProjection(projection)
  
        fs = getFeatureSetForGeoprocess(store, filterExpression, hexa, geomName)

        #start = time.time()
        count= fs.getSize()
        #print "Time..after: ", time.time() -  start
        
        if addEmptyGrids==False and count==0:
          continue
        newFeature = output.createNewFeature()
        newFeature["ID"]=id_
        newFeature["GEOMETRY"]=hexa
        newFeature["TOTAL"]=totalSize
        newFeature["COUNT"]=count
        newFeature["PERC"]=(count/totalSize)*100

        output.insert(newFeature)
        id_+=1
        
  else:
      increX = lado*0.5
      increY = (pow((pow(lado,2)-pow(lado*0.5,2)),0.5))
      numero_filas=int(dY/(increY*2))+1
      numero_columnas=int(dX/(lado*1.5))+2
  
      #Coordenadas del centro del 1er hexagono
      c1X = infX + increX
      c1Y = infY + increY
  
      numero_filas+=1
      self.setRangeOfValues(0,int(numero_filas*numero_columnas))
      for i in range(0, numero_columnas):
          if i%2 == 0:
              numero_filas-=1
          else:
              numero_filas+=1 #
          for j in range(0, numero_filas):
              if self.isCanceled():
                break
              else:
                self.setCurValue(n)
                n+=1
                self.setProgressText("Processing "+str(n)+" in "+str(int(numero_filas*numero_columnas))+" features")
              if i%2 == 0:
                  cX = c1X + (lado*1.5)*i
                  cY = c1Y + 2*increY*j
              else:
                  cX = c1X + (lado*1.5)*i
                  cY = c1Y + 2*increY*j - increY
              p1 = geom.createPoint(geom.D2, cX-increX, cY-increY)
              p2 = geom.createPoint(geom.D2, cX-lado, cY)
              p3 = geom.createPoint(geom.D2, cX-increX, cY+increY)
              p4 = geom.createPoint(geom.D2, cX+increX, cY+increY)
              p5 = geom.createPoint(geom.D2, cX+lado, cY)
              p6 = geom.createPoint(geom.D2, cX+increX, cY-increY)
              hexa = geom.createPolygon(vertexes=[p1,p2,p3,p4,p5,p6,p1])
              hexa.setProjection(projection)
              
              fs = getFeatureSetForGeoprocess(store, filterExpression, hexa, geomName)
              
              count = 0
              for k in fs:
                  if k.getDefaultGeometry().intersects(hexa):
                      count += 1
              if addEmptyGrids==False and count==0:
                continue
              newFeature = output.createNewFeature()
              newFeature["ID"]=id_
              newFeature["GEOMETRY"]=hexa
              newFeature["TOTAL"]=totalSize
              newFeature["COUNT"]=count
              newFeature["PERC"]=(count/totalSize)*100
              output.insert(newFeature)
              id_+=1