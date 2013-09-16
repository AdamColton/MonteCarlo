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
    
class MemoryMC(object):
  """
  This technique does not work.
  The computation gained is
  1 / BF**2
  where BF is the branching factor of the game.
  for connectfour it's 2%
  for Chess its 0.05%
  for Go it's 0.0013%
  """
  def __init__(self):
    self.memo = {}
  def move(self, game):
    moves = game.getMoves()
    moveRecord = {i:[1.0, 0.0] for i in moves}
    boards = {i:game.copy() for i in moves}
    positions = 0
    for move in moves:
      boards[move].move(move)
      key = boards[move].boardId()
      if key in self.memo:
        moveRecord[move] = self.memo[key]
      positions += 1
    self.memo = {}
    i = 0
    lenMoves = len(moves)
    while positions < config.positions :
      move = moves[i]
      sim = boards[move].copy()
      monkeyCarlo(sim) # make random opponent move
      monkeyCarlo(sim) # make our move
      key = sim.boardId()
      positions += fullMonkeyCarloGame(sim) + 2
      self.memo[key] = self.memo.get(key, [1.0, 0.0])
      self.memo[key][0] += 1
      moveRecord[move][0] += 1
      v = moveValue(game, sim)
      self.memo[key][1] += v
      moveRecord[move][1] += v
      i = (i + 1) % lenMoves
    results = [(moveRecord[move][1] / moveRecord[move][0], move) for move in moves]
    results.sort()
    game.move( results[-1][1] )
    
def getBook():
  try:
    file = open("book.txt",'r')
  except FileNotFoundError:
    return {}
  bookStr = file.read()
  file.close()
  book = {}
  for line in bookStr.split('\n'):
    try:
      vals = [int(val) for val in line.split(',')]
      book[vals[0]] = [vals[1], vals[2]]
    except ValueError:
      """
      Transient error I believe is related to reading and writing
      simultaneously. Skipping one table entry should not significantly
      effect the outcome of the game.
      """
      pass
  return book

class BookMC(object):
  def __init__(self):
    self.book = getBook()
  def move(self, game):
    moves = game.getMoves()
    moveRecord = {}
    boards = {i:game.copy() for i in moves}
    positions = 0
    for move in moves:
      boards[move].move(move)
      id = boards[move].boardId()
      moveRecord[id] = [1.0,0.0]
      if id in self.book:
        moveRecord[id][0] = self.book[id][0]
        moveRecord[id][1] = self.book[id][1]
      positions += 1
    i = 0
    lenMoves = len(moves)
    while positions < config.positions :
      move = moves[i]
      sim = boards[move].copy()
      id = sim.boardId()
      positions += fullMonkeyCarloGame(sim)
      moveRecord[id][0] += 1
      moveRecord[id][1] += moveValue(game, sim)
      i = (i + 1) % lenMoves
    results = [(moveRecord[boards[move].boardId()][1] / moveRecord[boards[move].boardId()][0], move) for move in moves]
    results.sort()
    game.move( results[-1][1] )