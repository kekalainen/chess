import random
import time


class AI:
    """A class which functions as a computer opponent for chess."""

    def __init__(self, game, difficulty=0):
        self.game = game
        self.difficulty = difficulty

    def random_move(self):
        """Returns a random move from a specified list of moves."""
        from_xy = random.choice(list(self.game.legal_moves.keys()))
        to_xy = random.choice(self.game.legal_moves[from_xy])
        return (from_xy, to_xy)

    def capturing_move(self, moves):
        """Returns a move which captures the most valuable piece possible from a specified list of moves."""
        value = -1
        move_options = []
        for from_xy in moves.keys():
            for to_xy in moves[from_xy]:
                captured_piece = self.game.board.get_piece(to_xy[0], to_xy[1])
                if captured_piece:
                    if captured_piece.value > value:
                        move_options = [(from_xy, to_xy)]
                        value = captured_piece.value
                    else:
                        move_options.append((from_xy, to_xy))
        return (value, random.choice(move_options) if move_options else None)

    def best_move(self, moves):
        """Returns the best move from a specified list of moves."""
        value = 0
        capturing_move = self.capturing_move(moves)
        if capturing_move[0] > value:
            value = capturing_move[0]
            move = capturing_move[1]
        else:
            move = self.random_move()
        return (value, move)

    def choose_move(self):
        """Returns a move from the game's current legal moves."""
        if self.game.legal_moves:
            if self.difficulty == 0:
                time.sleep(0.4)
                return self.random_move()
            if self.difficulty == 1:
                time.sleep(0.4)
                return self.best_move(self.game.legal_moves)[1]
        return None
