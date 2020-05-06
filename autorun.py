# encoding: utf-8
import gvsig
from gvsig import getResource
from java.io import File
from org.gvsig.tools import ToolsLocator


try:
  from addons.PointDensityGrid.pointDensityGridGeoprocess import PointDensityGridGeoprocess
except:
  import sys
  ex = sys.exc_info()[1]
  gvsig.logger("Can't load module 'PointDensityGridGeoprocess'. " + str(ex), gvsig.LOGGER_WARN)#, ex)
  PointDensityGridGeoprocess = None


# Icon made by [author link] from www.flaticon.com

def i18nRegister():
    i18nManager = ToolsLocator.getI18nManager()
    i18nManager.addResourceFamily("text",File(getResource(__file__,"i18n")))
  
def main(*args):
  if PointDensityGridGeoprocess== None:
    return
  i18nRegister()
  process = PointDensityGridGeoprocess()
  process.selfregister("Scripting")
  process.updateToolbox()

