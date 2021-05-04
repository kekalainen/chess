from string import ascii_lowercase
import re

from game.board import Board


class Game:
    """A class for handling game logic and state. Contains a board for keeping track of pieces."""

    def __init__(self, on_update):
        """Initializes a game and creates a board.

        Args:
            on_update: A callback function that is invoked when the game state changes.
        """
        self.white_to_move = True
        self.board = Board()
        self.on_update = on_update
        self.generate_legal_moves()
        self.an_moves = []

    def dispatch_update(self):
        if self.on_update:
            self.on_update()

    def generate_all_moves(self, white_to_move):
        """Generates all legal moves for the specified player, ignoring checks."""

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
        """Determines if the opponent can move a piece to the given coordinates."""
        opponent_moves = self.generate_all_moves(not self.white_to_move)
        for from_xy in opponent_moves:
            for to_xy in opponent_moves[from_xy]:
                if to_xy == xy:
                    return True
        return False

    def is_in_check(self):
        """Determines if the current player's king is in check."""
        king_xy = self.board.get_king_coordinates(self.white_to_move)
        return self.is_under_attack(king_xy)

    def generate_legal_moves(self):
        """Generates all legal moves for the current player."""

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
        """Switches the color to make the next move."""
        self.white_to_move = not self.white_to_move

    def store_move_an(self, move, previous_legal_moves):
        """Stores a move in algebraic notation."""

        an = move.piece.name.upper()
        if an == "P":
            an = ""

        # Specify initial column, file or both for ambiguous moves.
        ambiguous_moves = []
        for from_xy in previous_legal_moves:
            if (
                from_xy != (move.from_x, move.from_y)
                and self.board.get_piece(from_xy[0], from_xy[1]).name == move.piece.name
            ):
                for to_xy in previous_legal_moves[from_xy]:
                    if to_xy == (move.to_x, move.to_y):
                        ambiguous_moves.append(from_xy)
        if ambiguous_moves:
            ambiguous_x = ambiguous_y = False

            for from_xy in ambiguous_moves:
                if from_xy[0] == move.from_x:
                    ambiguous_x = True
                elif from_xy[1] == move.from_y:
                    ambiguous_y = True

            if ambiguous_x and ambiguous_y:
                an += ascii_lowercase[move.from_x] + str(self.board.width - move.from_y)
            else:
                if ambiguous_x:
                    an += str(self.board.width - move.from_y)
                if ambiguous_y:
                    an += ascii_lowercase[move.from_x]

        if move.captured_piece:
            an += "x"

        an += ascii_lowercase[move.to_x] + str(self.board.width - move.to_y)

        if self.check:
            if self.checkmate:
                an += "#"
            else:
                an += "+"

        self.an_moves.append(an)

    def move_piece(self, from_xy, to_xy):
        """Moves a piece and switches the color to move next if the move is legal."""
        if from_xy in self.legal_moves and to_xy in self.legal_moves[from_xy]:
            if self.board.move_piece(from_xy, to_xy):
                self.switch_color_to_move()
                previous_legal_moves = self.legal_moves
                self.generate_legal_moves()
                self.store_move_an(self.board.moves[-1], previous_legal_moves)
                self.dispatch_update()
                return True
        return False

    def move_piece_an(self, an):
        """Applies a move described in algebraic notation."""
        matches = re.search("([A-Z]?)([a-w]?)([0-9]?)x?([a-z][0-9])", an)
        match_to = matches.group(4)

        to_x = ascii_lowercase.index(match_to[0])
        to_y = self.board.width - int(match_to[1])

        piece_name = matches.group(1) or "P"
        from_x = matches.group(2)
        from_y = matches.group(3)

        for from_xy in self.legal_moves:
            if self.board.get_piece(from_xy[0], from_xy[1]).name.upper() == piece_name:
                for to_xy in self.legal_moves[from_xy]:
                    if to_xy == (to_x, to_y):
                        if not from_x and not from_y:
                            from_x = from_xy[0]
                            from_y = from_xy[1]
                            break
                        elif not from_x:
                            if from_y == from_xy[1]:
                                from_x = from_xy[0]
                                break
                        else:
                            if from_x == from_xy[0]:
                                from_y = from_xy[1]
                                break

        self.move_piece((from_x, from_y), (to_x, to_y))

    def undo_move(self):
        """Undoes the previous move and switches the color to move next if a previous move exists."""
        if self.board.undo_move():
            self.switch_color_to_move()
            self.generate_legal_moves()
            self.an_moves.pop()
            self.dispatch_update()
            return True
        return False
