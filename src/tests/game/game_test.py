import unittest
from game.board import Board
from game.game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(None)

    def test_get_legal_moves_empty_list_for_empty_tile(self):
        self.assertEqual(self.game.get_legal_moves(3, 3), [])

    def test_get_legal_moves_white_pawn(self):
        self.assertEqual(
            self.game.get_legal_moves(
                self.game.board.width // 2, self.game.board.width - 2
            ),
            [
                (self.game.board.width // 2, self.game.board.width - 3),
                (self.game.board.width // 2, self.game.board.width - 4),
            ],
        )
