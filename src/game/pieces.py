class Piece:
    def __init__(self, white: bool):
        if not white:  # black
            self.name = self.name.lower()


class Pawn(Piece):
    name = "P"
