class Enum:
  def __init__(self, *args):
    self._enum = args
  def __getattr__(self,name):
    return self._enum.index(name)
    
DisplayOptions = Enum("none", "dot", "summary", "verbose")