class Piece:
    """A base class for classes representing chess pieces."""

    horizontal = True
    vertical = True
    diagonal = True
    can_move_over_other_pieces = False
    range = 1

    def __init__(self, white: bool, board_width: int):
        if not white:  # black
            self.name = self.name.lower()
        self.board_width = board_width
        if self.range == float("inf"):
            self.range = self.board_width

    def is_white(self):
        return self.name.isupper()

    def moves(self):
        """Returns the relative moves for the piece."""
        moves = []
        for x in range(-self.range, self.range + 1):
            for y in range(-self.range, self.range + 1):
                if self.diagonal and abs(x) == abs(y):
                    moves.append((x, y))
                elif self.horizontal and x == 0:
                    moves.append((x, y))
                elif self.vertical and y == 0:
                    moves.append((x, y))
        return moves

    def is_legal_move(self, from_xy, to_xy, occupant):
        """Determines if the supplied relative move is defined for this piece."""
        return (to_xy[0] - from_xy[0], to_xy[1] - from_xy[1]) in self.moves()


class Pawn(Piece):
    name = "P"

    def moves(self):
        return (
            [(0, -1), (0, -2), (-1, -1), (1, -1)]
            if self.is_white()
            else [(0, 1), (0, 2), (-1, 1), (1, 1)]
        )

    def is_legal_move(self, from_xy, to_xy, occupant):
        if not Piece.is_legal_move(self, from_xy, to_xy, occupant):
            return False

        # Can move two tiles vertically only from initial position.
        if abs(from_xy[1] - to_xy[1]) > 1:
            if self.is_white():
                if from_xy[1] != self.board_width - 2:
                    return False
            elif from_xy[1] != 1:
                return False

        if from_xy[0] - to_xy[0] == 0:
            # Cannot capture a piece without moving horizontally.
            if occupant:
                return False
        # Must capture a piece if moving horizontally.
        elif not occupant:
            return False

        return True


class Knight(Piece):
    name = "N"
    can_move_over_other_pieces = True

    def moves(self):
        return [(-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2), (-2, -1), (-2, 1)]


class Bishop(Piece):
    name = "B"
    horizontal = False
    vertical = False
    range = float("inf")


class Rook(Piece):
    name = "R"
    diagonal = False
    range = float("inf")


class Queen(Piece):
    name = "Q"
    range = float("inf")


class King(Piece):
    name = "K"

    def moves(self):
        return Piece.moves(self) + [(-2, 0), (2, 0)]
