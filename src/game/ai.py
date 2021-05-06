import random
import time


class AI:
    """A class which functions as a computer opponent for chess."""

    def __init__(self, game, difficulty=0):
        self.game = game
        self.difficulty = difficulty

    def choose_move(self):
        """Returns a move from the game's current legal moves."""
        if self.game.legal_moves:
            if self.difficulty == 0:
                time.sleep(0.4)
                from_xy = random.choice(list(self.game.legal_moves.keys()))
                to_xy = random.choice(self.game.legal_moves[from_xy])
                return (from_xy, to_xy)
        return None
