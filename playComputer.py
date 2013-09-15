import random
from libs import connectfour
from libs import montecarlo
from config import PlayComputer as config
from libs.enums import DisplayOptions

class HI(object):
  def move(self, game):
    print(game)
    move = int( input("Move: ") )
    if move < 0 or move > 6 :
      self.error(game)
    else:
      if not game.move(move): self.error(game)
  def error(self, game):
    print("Invalid Move")
    self.move(game)
      
ais = (HI, getattr(montecarlo, config.ai))

firstMove = int( input("0: Me\n1: Computer\n2: Random\nWho goes first? ") )
if firstMove < 0 or firstMove > 1 : firstMove = random.randint(0,1)

players = [ais[0](), ais[1]()]
if firstMove == 1:
  players.append(players.pop(0))
  
game = connectfour.Game()
while not game.gameOver:
  player = players.pop(0)
  player.move(game)
  players.append(player)

print(game)
if (game.winner == game.players.two) != (firstMove == 1):
  print("You Lose")
else:
  print("You Win")