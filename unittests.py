import unittest
from libs.connectfour import Game
from libs.montecarlo import MonteCarlo

class TestConnectFour(unittest.TestCase):
  def test_createBoard(self):
    game = Game()
  def test_twoMove(self):
    game = Game()
    self.assertTrue(game.move(3))
    self.assertTrue(game.move(3))
    self.assertEqual(Game.players.one, game.board[0][3])
    self.assertEqual(Game.players.two, game.board[1][3])
  def test_verticalWin(self):
    game = Game()
    for i in range(4):
      game.move(6)
      game.move(i)
    self.assertEqual(game.winner, Game.players.one)
    self.assertTrue(game.gameOver)
  def test_horizontalWin(self):
    game = Game()
    for i in range(4):
      game.move(i)
      game.move(6)
    self.assertEqual(game.winner, Game.players.one)
    self.assertTrue(game.gameOver)
  def test_diagonalWin(self):
    game = Game()
    for i in range(16):
      game.move(i % 5)
    self.assertEqual(game.winner, Game.players.two)
    self.assertTrue(game.gameOver)
  def test_getMoves(self):
    game = Game()
    for i in range(6):
      game.move(0)
    self.assertEqual(game.getMoves(), [i for i in range(1,7)])
    
class TestMonteCarlo(unittest.TestCase):
  def test_montecarlo(self):
    game = Game()
    ai = MonteCarlo()
    ai.move(game)
    
unittest.main()
