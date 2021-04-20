class Piece:
    horizontal = True
    vertical = True
    diagonal = True
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
        moves = []
        h = self.range if self.horizontal else 1
        v = self.range if self.vertical else 1
        for x in range(-h if self.horizontal else 0, h if self.horizontal else 1):
            for y in range(-v if self.vertical else 0, v if self.vertical else 1):
                if self.diagonal:
                    if abs(x) != abs(y):
                        continue
                elif x != 0 and y != 0:
                    continue
                moves.append((x, y))
        return moves

    def is_legal_move(self, from_xy, to_xy, occupant):
        # Ensure the relative move is defined for this piece.
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


class Rook(Piece):
    name = "R"
    diagonal = False
    range = float("inf")
