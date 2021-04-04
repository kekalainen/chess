import unittest
from game.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_get_piece_empty_tile(self):
        self.assertEqual(self.board.get_piece(4, 4), None)

    def test_get_piece_occupied_tile(self):
        self.assertEqual(self.board.get_piece(0, 6).name, "P")

    def test_move_piece_duplicate_coordinates(self):
        self.assertFalse(self.board.move_piece((0, 1), (0, 1)))

    def test_move_piece(self):
        piece = self.board.get_piece(0, 1)
        self.assertTrue(self.board.move_piece((0, 1), (0, 2)))
        self.assertEqual(self.board.get_piece(0, 2), piece)
