import random
import math
from config import MonteCarlo as config
"""
Carlo the Monkey
       __
  w  c(..)o   (
   \__(-)    __)
       /\   (
      /(_)___)
      w /|
       | \
      m  m
"""
def monkeyCarlo(game):
  game.move( random.choice(game.getMoves()) )
  
def fullMonkeyCarloGame(game):
  moveCountT0 = game.moveCount
  while not game.gameOver:
    monkeyCarlo(game)
  moves = game.moveCount - moveCountT0
  """
  In the edge case that all moves being evaluated are winning moves
  (which becomes probable with the pruning AIs) we can get into a state
  where no new boards are ever evaluated. To counter this, if monkeyCarlo
  game consumes no moves, we set it to one to burn down the stack
  """
  if moves == 0 : moves = 1
  return moves
  
def moveValue(startingGame, endingPosition):
  if endingPosition.winner == startingGame.turn:
    return 1
  elif endingPosition.winner == startingGame.players.none:
    return config.drawWeight
  return 0
  
class MonkeyCarlo(object):
  def move(self, game):
    monkeyCarlo(game)

class MonteCarlo(object):
  def move(self, game):
    moves = game.getMoves()
    moveRecord = {i:[1.0, 0.0] for i in moves}
    positionsCount = 0
    
    for _ in range(config.simulations):    
      move = random.choice(moves)
      sim = game.copy()
      sim.move(move)
      moveRecord[move][0] += 1
      fullMonkeyCarloGame(sim)
      moveRecord[move][1] += moveValue(game, sim)
    results = [(moveRecord[move][1] / moveRecord[move][0], move) for move in moves]
    results.sort()
    game.move( results[-1][1] )
    
class CcMonteCarlo(object):
  """
  Constant Compute Monte Carlo
  Rather than running a consistent number of simulations, CCMC
  will evaluate a constant number of board positions, producing
  a nearly constant evaluation time
  """
  def move(self, game):
    moves = game.getMoves()
    moveRecord = {i:[1.0, 0.0] for i in moves}
    boards = {i:game.copy() for i in moves}
    positions = 0
    for move in moves:
      boards[move].move(move)
      positions += 1
    i = 0
    lenMoves = len(moves)
    while positions < config.positions :
      move = moves[i]
      sim = boards[move].copy()
      positions += fullMonkeyCarloGame(sim)
      moveRecord[move][0] += 1
      moveRecord[move][1] += moveValue(game, sim)
      i = (i + 1) % lenMoves
    results = [(moveRecord[move][1] / moveRecord[move][0], move) for move in moves]
    results.sort()
    game.move( results[-1][1] )
    
class PruningMC(object):
  def move(self, game):
    moves = game.getMoves()
    moveRecord = {i:[1.0, 0.0] for i in moves}
    boards = {i:game.copy() for i in moves}
    positions = 0
    for move in moves:
      boards[move].move(move)
      positions += 1 # keeping it honest
      
    i = 0
    lenMoves = len(moves)
    halvingStepSize = config.positions / 2
    nextHalving = halvingStepSize
    
    while positions < config.positions :
      if (positions > nextHalving):
        if (lenMoves != 2):
          halvingStepSize *= 0.5
          nextHalving += halvingStepSize
          results = [(moveRecord[move][1] / moveRecord[move][0], move) for move in moves]
          results.sort()
          lenMoves = math.ceil(lenMoves/2)
          moves = [move[1] for move in results[-lenMoves:]]
          i %= lenMoves
        else:
          nextHalving = config.positions
      move = moves[i]
      sim = boards[move].copy()
      positions += fullMonkeyCarloGame(sim)
      moveRecord[move][0] += 1
      moveRecord[move][1] += moveValue(game, sim)
      i = (i + 1) % lenMoves
    results = [(moveRecord[move][1] / moveRecord[move][0], move) for move in moves]
    results.sort()
    game.move( results[-1][1] )