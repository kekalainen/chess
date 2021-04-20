from game.pieces import Pawn, Rook
from game.move import Move


class Board:
    def __init__(self):
        self.width = 8
        self.moves = []
        self.pieces = [[None] * self.width for i in range(self.width)]
        for t in [(1, False), (6, True)]:
            for x in range(self.width):
                self.pieces[x][t[0]] = Pawn(t[1], self.width)
        for t in [(0, False), (self.width - 1, True)]:
            for x in [0, self.width - 1]:
                self.pieces[x][t[0]] = Rook(t[1], self.width)

    def is_in_bounds(self, x, y):
        return x < self.width and y < self.width

    def get_piece(self, x, y):
        if not self.is_in_bounds(x, y):
            return None
        return self.pieces[x][y]

    def is_legal_move(self, from_xy, to_xy):
        if from_xy == to_xy:
            return False

        if not self.is_in_bounds(to_xy[0], to_xy[1]):
            return False

        piece = self.get_piece(from_xy[0], from_xy[1])

        if not piece:
            return False

        occupant = self.get_piece(to_xy[0], to_xy[1])

        # Cannot capture own pieces.
        if occupant and piece.is_white() == occupant.is_white():
            return False

        # Check piece-specific rules.
        if not piece.is_legal_move(from_xy, to_xy, occupant):
            return False

        # Ensure there are no other pieces between the moving piece and its destination.
        diff_x = from_xy[0] - to_xy[0]
        diff_y = from_xy[1] - to_xy[1]
        horizontal = 0 if diff_x == 0 else 1
        vertical = 0 if diff_y == 0 else 1
        positive_x = 1 if diff_x < 0 else -1
        positive_y = 1 if diff_y < 0 else -1
        for i in range(1, max(abs(diff_x), abs(diff_y))):
            if self.get_piece(
                from_xy[0] + (horizontal * i * positive_x if horizontal else 0),
                from_xy[1] + (vertical * i * positive_y if vertical else 0),
            ):
                return False

        return True

    def get_legal_moves(self, x, y):
        piece = self.get_piece(x, y)
        if not piece:
            return []
        moves = piece.moves()
        legal_moves = []
        for move in moves:
            move_relative = (move[0] + x, move[1] + y)
            if self.is_legal_move((x, y), move_relative):
                legal_moves.append(move_relative)
        return legal_moves

    def move_piece(self, from_xy, to_xy):
        if not self.is_legal_move(from_xy, to_xy):
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
