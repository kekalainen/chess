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

    def test_store_move_an_kings_pawn(self):
        self.game.board.move_piece((4, 6), (4, 5))
        move = self.game.board.moves[-1]
        self.game.board.undo_move()
        self.game.store_move_an(move, self.game.legal_moves)
        self.assertEqual(self.game.an_moves[-1], "e3")

    def test_store_move_an_ambiguous_move(self):
        for an in ["a4", "a5", "h4", "h5", "Ra3", "Ra6", "Rhh3"]:
            self.game.move_piece_an(an)
        self.assertEqual(self.game.an_moves[-1], "Rhh3")

    def test_move_piece_an_kings_pawn(self):
        self.assertIsNone(self.game.board.get_piece(4, 5))
        self.game.move_piece_an("e3")
        self.assertEqual(self.game.board.get_piece(4, 5).name, "P")

    def test_undo_move_restores_white_to_move(self):
        self.game.move_piece_an("e3")
        white_to_move = self.game.white_to_move
        self.game.undo_move()
        self.assertEqual(self.game.white_to_move, not white_to_move)
