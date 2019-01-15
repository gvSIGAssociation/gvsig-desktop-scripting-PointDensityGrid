# encoding: utf-8
#from org.gvsig.expressionevaluator.impl import SQLSymbolTable

import gvsig
from gvsig import geom
from org.gvsig.fmap.dal import DALLocator
from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator

def main(*args):
  # Test pq con original phrase no funciona
  store = gvsig.currentLayer().getFeatureStore()
  dm = DALLocator.getDataManager()
  filterExpression = ExpressionEvaluatorLocator.getManager().createExpression()
  filterExpression.setPhrase("")
  spatialGeometry = geom.createGeometryFromWKT("POLYGON ((-74.26662451007567 40.497289998, -74.26662451007567 40.517289997999995, -74.24930400199999 40.527289998, -74.2319834939243 40.517289997999995, -74.2319834939243 40.497289998, -74.24930400199999 40.487289997999994, -74.26662451007567 40.497289998))")
  spatialGeometry.setProjection(gvsig.currentLayer().getProjection())
  
  ## store, exp, spatialGeometry
  print "Spatial"
  builder = ExpressionEvaluatorLocator.getManager().createExpressionBuilder()
  """
  expr1 = builder.and(
      builder.custom(exp.getPhrase()),
      builder.ST_Intersects(
        builder.geometry(spatialGeometry),
        builder.column("GEOMETRY")
      )
  ).toString()
  """
  expr1 = builder.ST_Intersects(
      builder.geometry(spatialGeometry),
      builder.column("GEOMETRY")
    ).toString()
  ## Creating new expression
  eva = ExpressionEvaluatorLocator.getManager().createExpression()
  eva.setPhrase(expr1)
  evaluator = DALLocator.getDataManager().createExpresion(eva)
  
  # Query
  fq = store.createFeatureQuery()
  fq.addFilter(evaluator)
  fq.retrievesAllAttributes()
  fset = store.getFeatureSet(fq)
  print "SIZE: ",fset.getSize()

  ### Reusing expression
  
  cloneExpression = filterExpression.clone()
  print "not cloning"
  cloneExpression.setPhrase(expr1)
  evaluator = DALLocator.getDataManager().createExpresion(cloneExpression)
  
  ## Query
  fq = store.createFeatureQuery()
  fq.addFilter(evaluator)
  fq.retrievesAllAttributes()
  fset = store.getFeatureSet(fq)
  print "SIZE: ",fset.getSize()
  
  
def main2(*args):
  store = gvsig.currentLayer().getFeatureStore()
  dm = DALLocator.getDataManager()
  i="True"
  evaluator = dm.createExpresion(i)
  fq = store.createFeatureQuery()
  fq.addFilter(evaluator)
  fq.retrievesAllAttributes()
  fset = store.getFeatureSet(fq)
  count = 0
  for f in fset:
    count+=1
  print count
  ###
  print "Spatial"
  spatialGeometry = geom.createGeometryFromWKT("POLYGON ((-74.26662451007567 40.497289998, -74.26662451007567 40.517289997999995, -74.24930400199999 40.527289998, -74.2319834939243 40.517289997999995, -74.2319834939243 40.497289998, -74.24930400199999 40.487289997999994, -74.26662451007567 40.497289998))")
  spatialGeometry.setProjection(gvsig.currentLayer().getProjection())
  builder = ExpressionEvaluatorLocator.getManager().createExpressionBuilder()
  expr1 = builder.and(
      builder.custom(i),
      builder.ST_Intersects(
        builder.geometry(spatialGeometry),
        builder.column("GEOMETRY")
      )
  ).toString()
  eva = ExpressionEvaluatorLocator.getManager().createExpression()
  eva.setPhrase(expr1)
  
  evaluator = DALLocator.getDataManager().createExpresion(eva)
  fq = store.createFeatureQuery()
  fq.addFilter(evaluator)
  fq.retrievesAllAttributes()
  fset = store.getFeatureSet(fq)
  count = 0
  for f in fset:
    count+=1
  print count
  
  
def main1(*args):
    from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
    manager = ExpressionEvaluatorLocator.getManager()
    symbolTable = manager.createSymbolTable()
    symbolTable.addVar("A", 2)
    expression = "[A]"
    code = manager.compile(expression)
    out = manager.evaluate(symbolTable, code)
    print out, type(out)
    

#class MyTable(SQLSymbolTable):
#    pass

class Hola:
    def set(self,dic):
        self.dic = dic
    def exists(self,name):
        return name in self.dic
    def value(self,name):
        return 0
    def itervars(self):
        return None

def main1(*args):

    from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator

    manager = ExpressionEvaluatorLocator.getManager()
    interpreter = manager.createInterpreter()
    #print interpreter
    symbolTable = manager.createSymbolTable()
    symbolTable.addVar("A", 2)
    symbolTable.addVar("B", 3)
    
    expression = "COS(0)"
    code = manager.compile(expression)
    
    symbol = interpreter.getSymbolTable()
    symbol  = MyTable()

    interpreter.setSymbolTable(symbol)
    out = interpreter.run(code)
    print out
    
def main3(*args):

    from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator

    manager = ExpressionEvaluatorLocator.getManager()
    expression = "COS(0)"
    evaluator = manager.createEvaluator(expression)
    print evaluator.getSymbolTable()
    symbolTable = manager.createSymbolTable()
    symbolTable.addVar("A", 2)
    symbolTable.addVar("B", 3)
    evaluator.setSymbolTable(symbolTable)
    print evaluator.compile()

def main4(*args):
    from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
    manager = ExpressionEvaluatorLocator.getManager()
    symbols = manager.createSymbolTable()
    interpreter = manager.createInterpreter()
    symbols.setSymbolTable(interpreter.getSymbolTable())
    interpreter.setSymbolTable(symbols)

    expression = "n*sin(90)"
    code = manager.compile(expression)

    symbols.addVar("n",5)
    out = interpreter.run(code)
    print out