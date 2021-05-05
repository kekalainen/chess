from game.pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from game.move import Move


class Board:
    """A class that represents a chess board."""

    def __init__(self):
        self.width = 8
        self.moves = []
        self.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.promotion_piece = "Q"

    def clear_pieces(self):
        """Removes all pieces from the board."""
        self.pieces = [[None] * self.width for i in range(self.width)]

    def set_piece(self, x, y, piece):
        """Places a piece on the board."""
        if not isinstance(piece, Piece):
            return False
        self.pieces[x][y] = piece
        return True

    def remove_piece(self, x, y):
        """Removes a piece from the board."""
        self.pieces[x][y] = None

    def get_piece_by_name(self, name):
        """Gets a chess piece by its abbreviation."""
        white = name.isupper()
        name = name.upper()
        piece = None
        if name == "P":
            piece = Pawn(white, self.width)
        elif name == "N":
            piece = Knight(white, self.width)
        elif name == "B":
            piece = Bishop(white, self.width)
        elif name == "R":
            piece = Rook(white, self.width)
        elif name == "Q":
            piece = Queen(white, self.width)
        elif name == "K":
            piece = King(white, self.width)
        return piece

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
                    piece = self.get_piece_by_name(char)
                    self.set_piece(x, y, piece)
                    x += 1

    def is_in_bounds(self, x, y):
        """Determines if supplied coordinates are within the boundaries of the board."""
        return x >= 0 and x < self.width and y >= 0 and y < self.width

    def get_piece(self, x, y):
        """Returns a piece on the board."""
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

        # Set the occupant for an en passant capture.
        if piece.name.upper() == "P" and not occupant:
            if self.moves:
                previous_move = self.moves[-1]
                if (
                    abs(previous_move.from_y - previous_move.to_y) == 2
                    and previous_move.to_x == to_xy[0]
                    and previous_move.to_y == from_xy[1]
                ):
                    occupant = self.get_piece(to_xy[0], from_xy[1])
                    if occupant.name.upper() != "P":
                        occupant = None

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
        """Moves a piece if the move is legal, ignoring checks."""
        if not self.is_legal_move(from_xy, to_xy):
            return False
        piece = self.get_piece(from_xy[0], from_xy[1])
        captured_piece = self.get_piece(to_xy[0], to_xy[1])
        en_passant = False
        promoted_to_piece = None
        if piece.name.upper() == "P":
            if not captured_piece and from_xy[0] != to_xy[0]:
                captured_piece = self.get_piece(to_xy[0], from_xy[1])
                self.remove_piece(to_xy[0], from_xy[1])
                en_passant = True
            elif to_xy[1] == 0 or to_xy[1] == self.width - 1:
                promoted_to_piece = self.get_piece_by_name(self.promotion_piece if piece.is_white() else self.promotion_piece.lower())

        move = Move(
            piece,
            from_xy[0],
            from_xy[1],
            captured_piece,
            en_passant,
            to_xy[0],
            to_xy[1],
            promoted_to_piece,
        )
        self.remove_piece(move.from_x, move.from_y)
        if promoted_to_piece:
            piece = promoted_to_piece
        self.set_piece(move.to_x, move.to_y, piece)
        self.moves.append(move)
        return True

    def undo_move(self):
        """Moves a piece back to its previous position and returns any captured piece to the board."""
        if len(self.moves) > 0:
            move = self.moves.pop()
            self.pieces[move.from_x][move.from_y] = move.piece
            self.remove_piece(move.to_x, move.to_y)
            if move.captured_piece:
                if move.en_passant:
                    self.set_piece(move.to_x, move.from_y, move.captured_piece)
                else:
                    self.set_piece(move.to_x, move.to_y, move.captured_piece)
            return True
        return False
