from game.board import Board


class Game:
    def __init__(self, on_update):
        self.white_to_move = True
        self.board = Board()
        if on_update:
            self.dispatch_update = on_update
        self.generate_legal_moves()

    def generate_all_moves(self, white_to_move):
        """Generate all legal moves for the specified player, ignoring checks."""

        all_moves = {}

        for y in range(self.board.width):
            for x in range(self.board.width):
                piece = self.board.get_piece(x, y)

                if not piece or piece.is_white() != white_to_move:
                    continue

                piece_moves = piece.moves()
                from_xy = (x, y)
                if not from_xy in all_moves:
                    all_moves[from_xy] = []
                for move in piece_moves:
                    to_xy = (move[0] + x, move[1] + y)
                    if self.board.is_legal_move(from_xy, to_xy):
                        all_moves[from_xy].append(to_xy)

        return all_moves

    def is_under_attack(self, xy):
        """Determine if the opponent can move a piece to the given coordinates."""
        opponent_moves = self.generate_all_moves(not self.white_to_move)
        for from_xy in opponent_moves:
            for to_xy in opponent_moves[from_xy]:
                if to_xy == xy:
                    return True
        return False

    def is_in_check(self):
        """Determine if the current player's king is in check."""
        king_xy = self.board.get_king_coordinates(self.white_to_move)
        return self.is_under_attack(king_xy)

    def generate_legal_moves(self):
        """Generate all legal moves for the current player."""

        all_moves = self.generate_all_moves(self.white_to_move)
        self.legal_moves = {}
        for from_xy in all_moves:
            self.legal_moves[from_xy] = []
            for to_xy in all_moves[from_xy]:
                self.board.move_piece(from_xy, to_xy)
                if not self.is_in_check():
                    self.legal_moves[from_xy].append(to_xy)
                self.board.undo_move()
            if not self.legal_moves[from_xy]:
                del self.legal_moves[from_xy]

        self.check = self.is_in_check()

        if len(self.legal_moves) == 0:
            if self.check:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

    def get_legal_moves(self, x, y):
        """Gets legal moves for the piece (if any) on the given coordinates."""
        return self.legal_moves[(x, y)] if (x, y) in self.legal_moves else []

    def switch_color_to_move(self):
        self.white_to_move = not self.white_to_move

    def move_piece(self, from_xy, to_xy):
        if from_xy in self.legal_moves and to_xy in self.legal_moves[from_xy]:
            if self.board.move_piece(from_xy, to_xy):
                self.switch_color_to_move()
                self.generate_legal_moves()
                self.dispatch_update()
                return True
        return False

    def undo_move(self):
        if self.board.undo_move():
            self.switch_color_to_move()
            self.generate_legal_moves()
            self.dispatch_update()
            return True
        return False
