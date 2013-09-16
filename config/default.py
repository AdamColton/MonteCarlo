from libs.enums import DisplayOptions

class MonteCarlo:
  drawWeight = 0.1
  simulations = 100
  positions = 8400
  
class Compete:
  ai1 = "MemoryMC"
  ai2 = "CcMonteCarlo"
  randomizeFirstMove = True
  games = 50
  display = DisplayOptions.verbose
  
class PlayComputer:
  ai = "PruningMC"