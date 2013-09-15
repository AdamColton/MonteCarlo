from libs.enums import DisplayOptions

class MonteCarlo:
  drawWeight = 0.1
  simulations = 100
  positions = 4200
  
class Compete:
  ai1 = "MonkeyCarlo"
  ai2 = "CcMonteCarlo"
  randomizeFirstMove = True
  games = 10
  display = DisplayOptions.dot
  
class PlayComputer:
  ai = "CcMonteCarlo"