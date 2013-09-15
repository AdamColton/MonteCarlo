import random
from libs import connectfour
from libs import montecarlo
from config import Compete as config
from libs.enums import DisplayOptions

ais = (getattr(montecarlo, config.ai1), getattr(montecarlo, config.ai2))
aiNames = (config.ai1, config.ai2)
scores = [0,0]

for _ in range(config.games):
  players = [ais[0](), ais[1]()]
  playersReversed = False
  if config.randomizeFirstMove and random.random() > 0.5:
    playersReversed = True
    players.append(players.pop(0))
    
  game = connectfour.Game()
  while not game.gameOver:
    player = players.pop(0)
    player.move(game)
    players.append(player)
  if config.display >= DisplayOptions.summary: print(game)
  if config.display == DisplayOptions.dot: print('.', end='', flush=True)
  increment = 0
  if (game.winner == game.players.two) != playersReversed : increment = 1
  scores[increment] += 1

if config.display == DisplayOptions.dot: print()
print(scores[0], " - ", config.ai1)
print(scores[1], " - ", config.ai2)