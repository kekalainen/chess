class Move:
    """A class which describes a single move in the game of chess."""
    
    def __init__(self, piece, from_x, from_y, captured_piece, to_x, to_y):
        self.piece = piece
        self.captured_piece = captured_piece
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
