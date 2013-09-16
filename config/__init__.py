from config.default import *
import sys
import inspect  
customConfig = True
try:
  from config import custom
except ImportError:
  customConfig = False
  
if customConfig:
  def mergeCustom(myClass, customClass):
    for key, value in customClass.__dict__.items():
      if not key.startswith("__"):
        setattr(myClass, key, value)
        
  getClasses = lambda module: { name:obj for name, obj in inspect.getmembers(sys.modules[module]) if inspect.isclass(obj) }
  myClasses = getClasses("config")
  customClasses = getClasses("config.custom")
  for myClassName, myClassObj in myClasses.items():
    if myClassName in customClasses: mergeCustom(myClassObj, customClasses[myClassName])