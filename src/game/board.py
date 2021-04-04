from game.pieces import Pawn
from game.move import Move


class Board:
    width = 8
    moves = []

    def __init__(self):
        self.pieces = [[None] * self.width for i in range(self.width)]
        for t in [(1, False), (6, True)]:
            for x in range(self.width):
                self.pieces[x][t[0]] = Pawn(t[1])

    def get_piece(self, x, y):
        return self.pieces[x][y]

    def move_piece(self, from_xy, to_xy):
        if from_xy == to_xy:
            return False
        piece = self.pieces[from_xy[0]][from_xy[1]]
        captured_piece = self.pieces[to_xy[0]][to_xy[1]]
        move = Move(piece, from_xy[0], from_xy[1], captured_piece, to_xy[0], to_xy[1])
        self.pieces[move.from_x][move.from_y] = None
        self.pieces[move.to_x][move.to_y] = piece
        self.moves.append(move)
        return True

    def undo_move(self):
        if len(self.moves) > 0:
            move = self.moves.pop()
            self.pieces[move.from_x][move.from_y] = move.piece
            self.pieces[move.to_x][move.to_y] = move.captured_piece
            return True
        return False
