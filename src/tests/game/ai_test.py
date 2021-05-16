import unittest
from game.game import Game


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.game = Game(ai_difficulty=1)

    def test_choose_move_returns_legal_move(self):
        move = self.game.ai.choose_move()
        self.assertIn(move[0], self.game.legal_moves)
        self.assertIn(move[1], self.game.legal_moves[move[0]])
