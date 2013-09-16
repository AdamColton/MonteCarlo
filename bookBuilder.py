from libs import montecarlo
from libs.connectfour import Game
from libs import multiprocHelpers
from config import BookBuilder as config
import math

import multiprocessing
  
def researchPosition(game):
  """
  Play each move a large (~100) number of times
  and return the win/loss record of the trials
  """
  moves = game.getMoves()
  moveRecord = {}
  for move in moves:
    gameMove = game.copy()
    gameMove.move(move)
    wins = 0
    for _ in range(config.researchDepth):
      sim = gameMove.copy()
      montecarlo.fullMonkeyCarloGame(sim)
      if sim.winner == game.turn : wins += 1
    moveRecord[gameMove.boardId()] = [config.researchDepth, wins]
  return moveRecord
  

def worker(responses):
  while True:
    ai = montecarlo.BookMC() #bootstrapping FTW
    game = Game()
    while not game.gameOver:
      responses.put( researchPosition(game) )
      ai.move(game)
    
def publish(book):
  booksStr = "\n".join( (",".join( (str(boardId), str(record[0]), str(record[1])) ) for boardId, record in book.items()) )
  file = open("book.txt",'w')
  file.write(booksStr)
  file.close()
  
if __name__ == '__main__' :
  book = montecarlo.getBook()
  responses = multiprocessing.JoinableQueue()
  for _ in  range( multiprocHelpers.calculateCores(config.cores) ):
    p = multiprocessing.Process(target=worker, args=(responses,))
    p.daemon = True
    p.start()
  while True:
    response = responses.get()
    for boardId, record in response.items():
      book[boardId] = book.get(boardId, [0,0]) #initilize if never seen before
      book[boardId][0] += record[0]
      book[boardId][1] += record[1]
    publish(book)
  