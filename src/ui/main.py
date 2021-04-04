import tkinter as tk
import tkinter.messagebox

from .board import BoardFrame
from game.board import Board


class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.board_tile_width = 100

        x = self.master.winfo_screenwidth() // 2 - 150
        y = self.master.winfo_screenheight() // 2 - 50
        self.master.geometry("%dx%d+%d+%d" % (300, 125, x, y))
        self.master.resizable(False, False)

        padx = 10
        pady = 5

        start_btn = tk.Button(self, text="Play", command=self.start_game)
        start_btn.grid(row=0, column=1, padx=padx, pady=pady)

        credits_btn = tk.Button(
            self,
            text="Credits",
            command=lambda: tk.messagebox.showinfo(
                title="Credits",
                message="%s by %s\n\nIcons:\n%s"
                % (
                    self.master.title(),
                    "Kekalainen (git@kekalainen.me)",
                    "Font Awesome Free 5.15.3 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0)",
                ),
            ),
        )
        credits_btn.grid(row=1, column=1, padx=padx, pady=pady)

        quit_btn = tk.Button(self, text="Quit", command=self.master.destroy)
        quit_btn.grid(row=2, column=1, padx=padx, pady=pady)

        self.grid()

    def start_game(self):
        if not hasattr(self, "board"):
            self.board = Board()
            dimension = self.board.width * self.board_tile_width
            self.board_window = tk.Toplevel(master=self)
            x = self.master.winfo_x() - dimension - 4
            y = self.master.winfo_y()
            self.board_window.geometry("%dx%d+%d+%d" % (dimension, dimension, x, y))
            self.board_window.resizable(False, False)
            self.board_frame = BoardFrame(
                self.board_window, board=self.board, tile_width=self.board_tile_width
            )
            self.master.bind("<Configure>", self.board_window_follow)
            self.board_window.protocol("WM_DELETE_WINDOW", self.on_board_window_close)

    def board_window_follow(self, event=None):
        x = self.master.winfo_x() - self.board_window.winfo_width() - 4
        y = self.master.winfo_y()
        self.board_window.geometry("+%d+%d" % (x, y))

    def on_board_window_close(self):
        delattr(self, "board")
        self.master.unbind("<Configure>")
        self.board_window.destroy()
