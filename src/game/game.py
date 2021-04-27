from game.board import Board


class Game:
    def __init__(self, on_update):
        self.white_to_move = True
        self.board = Board(self)
        self.dispatch_update = on_update
    
    def is_legal_move(self, from_xy, to_xy, piece, occupant):
        if piece.is_white() != self.white_to_move:
            return False
        return True
    
    def switch_color_to_move(self):
        self.white_to_move = not self.white_to_move
        self.dispatch_update()

    def move_piece(self, from_xy, to_xy):
        if self.board.move_piece(from_xy, to_xy):
            self.switch_color_to_move()
            return True
        return False
        
    def undo_move(self):
        if self.board.undo_move():
            self.switch_color_to_move()
            return True
        return False
