from os import path
import tkinter as tk
from PIL import Image, ImageTk

from game.pieces import Pawn, Knight, Bishop, Rook, Queen, King


class BoardFrame(tk.Frame):
    def __init__(self, master=None, game=None, tile_width=100):
        super().__init__(master)
        self.master = master
        self.game = game
        self.board = game.board

        self.pack(expand=tk.TRUE, fill=tk.BOTH)
        self.board_canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.board_canvas.pack(expand=tk.TRUE, fill=tk.BOTH)

        self.tile_width = tile_width
        self.canvas_base_offset = self.tile_width / 20
        self.tile_colors = ["#542E1D", "#EFD8B0"]
        self.selected_color = "#FF0000"

        self.selected_tile = None
        self.legal_tiles = []

        self.drawn_tiles = []
        self.drawn_pieces = []
        self.load_piece_images()
        self.draw_board()

        self.board_canvas.bind("<Button 1>", self.select_tile)
        master.bind("<Escape>", self.deselect_tile)
        master.bind("<Control-z>", self.undo_move)
        master.bind("<Control-Z>", self.undo_move)

    def load_piece_images(self):
        self.piece_images = {}
        img_dir_path = path.dirname(path.realpath(__file__)) + "/../img/pieces/"
        for color in ["w", "b"]:
            for piece in [Pawn, Knight, Bishop, Rook, Queen, King]:
                img_path = img_dir_path + piece.__name__.lower() + "_" + color + ".png"
                img = Image.open(img_path)
                dimension = self.tile_width / 10 * 7
                img.thumbnail((dimension, dimension))
                self.piece_images[
                    piece.name if color == "w" else piece.name.lower()
                ] = ImageTk.PhotoImage(img)

    def undo_move(self, event):
        self.game.undo_move()
        self.deselect_tile()
        self.draw_pieces()

    def draw_board(self):
        self.draw_tiles()
        self.draw_pieces()

    def draw_tiles(self):
        for tile in self.drawn_tiles:
            self.board_canvas.delete(tile)
        self.drawn_tiles = []

        for y in range(self.board.width):
            for x in range(self.board.width):
                outline_width = self.tile_width / 10
                x1 = x * self.tile_width
                x2 = x1 + self.tile_width - outline_width
                y1 = y * self.tile_width
                y2 = y1 + self.tile_width - outline_width
                outline = color = self.tile_colors[(x + y) % 2]
                if self.selected_tile == (x, y):
                    outline = self.selected_color
                elif (x, y) in self.legal_tiles:
                    outline = self.selected_color
                tile = self.board_canvas.create_rectangle(
                    x1 + self.canvas_base_offset,
                    y1 + self.canvas_base_offset,
                    x2 + self.canvas_base_offset,
                    y2 + self.canvas_base_offset,
                    width=outline_width,
                    outline=outline,
                    fill=color,
                )
                self.board_canvas.tag_lower(tile)
                self.drawn_tiles.append(tile)

    def draw_pieces(self):
        for piece in self.drawn_pieces:
            self.board_canvas.delete(piece)
        self.drawn_pieces = []

        for y in range(self.board.width):
            for x in range(self.board.width):
                if self.board.get_piece(x, y) != None:
                    img = self.piece_images[self.board.get_piece(x, y).name]
                    piece = self.board_canvas.create_image(
                        (
                            x * self.tile_width + (self.tile_width - img.width()) // 2,
                            y * self.tile_width + (self.tile_width - img.height()) // 2,
                        ),
                        anchor=tk.NW,
                        image=img,
                    )
                    self.drawn_pieces.append(piece)

    def select_tile(self, event):
        x = event.x // self.tile_width
        y = event.y // self.tile_width
        tile = (x, y)
        if not self.selected_tile:
            if self.board.get_piece(x, y):
                self.selected_tile = tile
                self.legal_tiles = self.board.get_legal_moves(x, y)
                self.draw_board()
        else:
            self.game.move_piece((self.selected_tile[0], self.selected_tile[1]), (x, y))
            self.deselect_tile()
            self.draw_pieces()

    def deselect_tile(self, event=None):
        self.selected_tile = None
        self.legal_tiles = []
        self.draw_tiles()
