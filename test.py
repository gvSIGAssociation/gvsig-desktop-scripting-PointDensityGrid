# encoding: utf-8

import gvsig
def main1(*args):
    from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
    manager = ExpressionEvaluatorLocator.getManager()
    symbolTable = manager.createSymbolTable()
    symbolTable.addVar("A", 2)
    expression = "[A]"
    code = manager.compile(expression)
    out = manager.evaluate(symbolTable, code)
    print out, type(out)
    
from org.gvsig.expressionevaluator.impl import SQLSymbolTable

class MyTable(SQLSymbolTable):
    pass

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

def main(*args):
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