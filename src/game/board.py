from game.pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from game.move import Move


class Board:
    def __init__(self):
        self.width = 8
        self.moves = []
        self.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def clear_pieces(self):
        self.pieces = [[None] * self.width for i in range(self.width)]

    def set_piece(self, x, y, piece):
        if not isinstance(piece, Piece):
            return False
        self.pieces[x][y] = piece
        return True

    def load_fen(self, fen):
        """Load a board position described in Forsyth–Edwards Notation."""
        self.clear_pieces()
        self.fen = fen
        x = y = 0
        for char in fen:
            if char.isnumeric():
                x += int(char)
            else:
                if char == "/":
                    x = 0
                    y += 1
                elif char == " ":
                    break
                else:
                    piece_name = char.upper()
                    if piece_name == "P":
                        piece = Pawn(char.isupper(), self.width)
                    elif piece_name == "N":
                        piece = Knight(char.isupper(), self.width)
                    elif piece_name == "B":
                        piece = Bishop(char.isupper(), self.width)
                    elif piece_name == "R":
                        piece = Rook(char.isupper(), self.width)
                    elif piece_name == "Q":
                        piece = Queen(char.isupper(), self.width)
                    elif piece_name == "K":
                        piece = King(char.isupper(), self.width)
                    self.set_piece(x, y, piece)
                    x += 1

    def is_in_bounds(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.width

    def get_piece(self, x, y):
        if not self.is_in_bounds(x, y):
            return None
        return self.pieces[x][y]

    def get_king_coordinates(self, white):
        """Gets the coordinates of the specified player's king."""
        for y in range(self.width):
            for x in range(self.width):
                piece = self.get_piece(x, y)
                if piece and piece.is_white() == white and piece.name.upper() == "K":
                    return (x, y)

    def is_legal_move(self, from_xy, to_xy):
        """Determines if a move is legal, ignoring checks."""

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
        if not piece.can_move_over_other_pieces:
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
