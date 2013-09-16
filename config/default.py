from libs.enums import DisplayOptions

class MonteCarlo:
  drawWeight = 0.1
  simulations = 100
  positions = 8400
  
class Compete:
  ai1 = "BookMC"
  ai2 = "CcMonteCarlo"
  randomizeFirstMove = True
  games = 100
  display = DisplayOptions.verbose
  
class PlayComputer:
  ai = "BookMC"
  
class BookBuilder:
  researchDepth = 100
  cores = -2