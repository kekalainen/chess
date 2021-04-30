import unittest
from game.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_get_piece_empty_tile(self):
        self.assertEqual(self.board.get_piece(4, 4), None)

    def test_get_piece_occupied_tile(self):
        self.assertEqual(self.board.get_piece(0, 6).name, "P")

    def test_get_piece_out_of_bounds(self):
        self.assertEqual(self.board.get_piece(0, self.board.width), None)

    def test_move_piece_duplicate_coordinates(self):
        self.assertFalse(self.board.move_piece((0, 1), (0, 1)))

    def test_move_piece(self):
        piece = self.board.get_piece(0, 1)
        self.assertTrue(self.board.move_piece((0, 1), (0, 2)))
        self.assertEqual(self.board.get_piece(0, 2), piece)

    def test_is_in_bounds_zero(self):
        self.assertTrue(self.board.is_in_bounds(0, 0))

    def test_is_in_bounds_exceeding_width(self):
        self.assertFalse(self.board.is_in_bounds(self.board.width, self.board.width))

    def test_is_legal_move_pawn_can_move_two_initially(self):
        self.assertTrue(self.board.is_legal_move((0, 1), (0, 3)))

    def test_is_legal_move_pawn_cannot_move_two_normally(self):
        self.board.move_piece((0, 1), (0, 2))
        self.assertFalse(self.board.is_legal_move((0, 2), (0, 4)))

    def test_undo_move_no_moves(self):
        self.assertFalse(self.board.undo_move())

    def test_undo_move_decrements_move_count(self):
        self.board.move_piece((0, 1), (0, 2))
        move_count = len(self.board.moves)
        self.board.undo_move()
        self.assertEqual(len(self.board.moves), move_count - 1)

    def test_undo_move_reverts_piece_position(self):
        self.board.move_piece((0, 1), (0, 2))
        self.assertIsNone(self.board.get_piece(0, 1))
        self.board.undo_move()
        self.assertIsNotNone(self.board.get_piece(0, 1))
