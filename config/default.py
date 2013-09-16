from libs.enums import DisplayOptions

class MonteCarlo:
  drawWeight = 0.1
  simulations = 100
  positions = 4200
  
class Compete:
  ai1 = "PruningMC"
  ai2 = "CcMonteCarlo"
  randomizeFirstMove = True
  games = 10
  display = DisplayOptions.verbose
  
class PlayComputer:
  ai = "PruningMC"