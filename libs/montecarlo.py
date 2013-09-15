import random
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
  return game.moveCount - moveCountT0
    
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
      if sim.winner == game.turn:
        moveRecord[move][1] += 1
      elif sim.winner == game.players.none:
        moveRecord[move][1] += config.drawWeight
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
      if sim.winner == game.turn:
        moveRecord[move][1] += 1
      elif sim.winner == game.players.none:
        moveRecord[move][1] += config.drawWeight
      i = (i + 1) % lenMoves
    results = [(moveRecord[move][1] / moveRecord[move][0], move) for move in moves]
    results.sort()
    game.move( results[-1][1] )