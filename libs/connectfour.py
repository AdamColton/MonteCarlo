import copy
from libs.enums import Enum

class Game(object):
  players = Enum("none","one","two")
  charMap = {
    players.none: ".",
    players.one: "X",
    players.two: "O"
  }
  swap = {
    players.one: players.two,
    players.two: players.one
  }
  def __init__(self):
    self.board = [ [0 for i in range(7)] for j in range(6) ]
    self.turn = Game.players.one
    self.gameOver = False
    self.winner = Game.players.none
    self.moveCount = 0
  def getMoves(self):
    return [i for i in range(7) if self.board[5][i] == Game.players.none]
  def move(self, x):
    # board[5][x] is the top of the board
    if (self.board[5][x] != Game.players.none or self.gameOver) : return False
    y = [i for i in range(6) if self.board[i][x] == Game.players.none][0]
    self.board[y][x] = self.turn
    self.moveCount += 1
    self.gameOver = self._checkForWin(x,y)
    if self.gameOver: self.winner = self.turn
    if self.moveCount == 42 : self.gameOver = True
    self.turn = Game.swap[self.turn]
    return True
  def _checkForWin(self,x,y):
    if self.moveCount < 6 : return False
    linesToTry = [
      [ (x, y-i) for i in range(4) if y-i >= 0 ],
      [ (i,y) for i in range(x-3, x+4) if i >=0 and i <=6 ],
      [ (x+i, y+i) for i in range(-3,4) if x+i >=0 and x+i <=6 and y+i >= 0 and y+i <= 5 ],
      [ (x+i, y-i) for i in range(-3,4) if x+i >=0 and x+i <=6 and y-i >= 0 and y-i <= 5 ]
    ]
    for lineToTry in linesToTry:
      count = 0
      for coord in lineToTry:
        if self.board[coord[1]][coord[0]] == self.turn:
          count += 1
          if (count == 4):
            return True
        else:
          count = 0
    return False
  def __str__(self):
    ret = [" " + " ".join( (Game.charMap[i] for i in row) ) for row in reversed(self.board)]
    ret.append(" - - - - - - - ")
    ret.insert(0," 0 1 2 3 4 5 6")
    return "\n".join(ret)
  def copy(self):
    return CopyGame(self)

class CopyGame(Game):
  def __init__(self, parent):
    self.board = copy.deepcopy(parent.board)
    self.turn = parent.turn
    self.gameOver = parent.gameOver
    self.winner = parent.winner
    self.moveCount = parent.moveCount