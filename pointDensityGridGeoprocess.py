# encoding: utf-8
from gvsig.uselib import use_plugin
use_plugin("org.gvsig.toolbox")
use_plugin("org.gvsig.geoprocess.app.mainplugin")

import gvsig
import pdb
from gvsig import geom
from gvsig import commonsdialog
from gvsig.libs.toolbox import ToolboxProcess, NUMERICAL_VALUE_DOUBLE,SHAPE_TYPE_POLYGON,NUMERICAL_VALUE_INTEGER,SHAPE_TYPE_POLYGON, SHAPE_TYPE_POINT
from es.unex.sextante.gui import core
from es.unex.sextante.gui.core import NameAndIcon
from es.unex.sextante.additionalInfo import AdditionalInfoVectorLayer

from es.unex.sextante.gui.core import SextanteGUI
from org.gvsig.geoprocess.lib.api import GeoProcessLocator

from addons.PointDensityGrid import pointDensityGrid
reload(pointDensityGrid)

from addons.PointDensityGrid.pdglib.hexa_grid import pointDensityGrid_hexa
from addons.PointDensityGrid.pdglib.square_grid import pointDensityGrid_square
from addons.PointDensityGrid.pointDensityGrid import pointDensityGridCreation
from addons.PointDensityGrid.pointDensityGrid import GRID_HEXAGON_HORIZONTAL,GRID_HEXAGON_VERTICAL,GRID_SQUARE
from org.gvsig.andami import PluginsLocator
import os
from java.io import File
from org.gvsig.tools import ToolsLocator

class PointDensityGridGeoprocess(ToolboxProcess):
  def getHelpFile(self):
    name = "pointdensitygrid"
    extension = ".xml"
    locale = PluginsLocator.getLocaleManager().getCurrentLocale()
    tag = locale.getLanguage()
    #extension = ".properties"

    helpPath = gvsig.getResource(__file__, "help", name + "_" + tag + extension)
    if os.path.exists(helpPath):
        return File(helpPath)
    #Alternatives
    alternatives = PluginsLocator.getLocaleManager().getLocaleAlternatives(locale)
    for alt in alternatives:
        helpPath = gvsig.getResource(__file__, "help", name + "_" + alt.toLanguageTag() + extension )
        if os.path.exists(helpPath):
            return File(helpPath)
    # More Alternatives
    helpPath = gvsig.getResource(__file__, "help", name + extension)
    if os.path.exists(helpPath):
        return File(helpPath)
    return None
  def defineCharacteristics(self):
      i18nManager = ToolsLocator.getI18nManager()
      self.setName(i18nManager.getTranslation("_Point_density_grid_geoprocess_name"))
      self.setGroup(i18nManager.getTranslation("_Data_Analysis"))
      self.setUserCanDefineAnalysisExtent(True)
      self.setRecalculateForCell(False)
      params = self.getParameters()
      params.addInputVectorLayer("LAYER",i18nManager.getTranslation("_Input_layer"), SHAPE_TYPE_POINT, True)
      #params.addInputVectorLayer("LAYER_ENVELOPE",i18nManager.getTranslation("_Input_layer_Envelope"), AdditionalInfoVectorLayer.SHAPE_TYPE_ANY, True)
      params.addNumericalValue("DISTANCEGRID", i18nManager.getTranslation("_Grid_distance"),0, NUMERICAL_VALUE_DOUBLE)
      params.addSelection("GRIDTYPE", i18nManager.getTranslation("_Grid_type"), 
                          [GRID_HEXAGON_HORIZONTAL, 
                           GRID_HEXAGON_VERTICAL,
                           GRID_SQUARE]);
      params.addBoolean("ADDEMPTYGRID", i18nManager.getTranslation("_Add_empty_grids"), True)
      #params.addString("EXPRESSION", i18nManager.getTranslation("_Value_expression"))
      params.addTableFilter("EXPRESSION", i18nManager.getTranslation("_Filter_expression"), "LAYER", True)
      self.addOutputVectorLayer("RESULT_POLYGON", "DensityGrid", SHAPE_TYPE_POLYGON)
      
  def processAlgorithm(self):
        features=None
        params = self.getParameters()
        sextantelayer = params.getParameterValueAsVectorLayer("LAYER")
        distancegrid = params.getParameterValueAsDouble("DISTANCEGRID")
        gridType = params.getParameterValueAsString("GRIDTYPE")
        addEmptyGrids = params.getParameterValueAsBoolean("ADDEMPTYGRID")
        filterExpression = params.getParameterValueAsObject("EXPRESSION")

        store = sextantelayer.getFeatureStore()
        projection = sextantelayer.getCRS()
        
        envelope = self.getAnalysisExtent()
        envelope = envelope.getAsRectangle2D()#envelope.getFullExtent() # Rectangle2D
        featureType = store.getDefaultFeatureType()
        geomName = featureType.getDefaultGeometryAttributeName()

        pointDensityGridCreation(self, store, gridType, distancegrid, addEmptyGrids, projection, envelope, filterExpression, geomName)

        return True
        
def main(*args):
        process = PointDensityGridGeoprocess()
        process.selfregister("Scripting")
        process.updateToolbox()

