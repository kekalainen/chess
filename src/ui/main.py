import tkinter as tk
import tkinter.messagebox
from tkinter.ttk import Notebook

from .board import BoardFrame
from game.game import Game


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

        tabs = Notebook(self)
        tabs.grid(row=0, column=0, sticky="NW")

        tabs_game = tk.Frame(tabs)
        tabs.add(tabs_game, text="Game")

        self.start_btn = tk.Button(tabs_game, text="Play", command=self.start_game)
        self.start_btn.grid(row=0, column=0, padx=padx, pady=pady)

        self.status_label = tk.Label(tabs_game, text="")
        self.status_label.grid(row=1, column=0, padx=padx, pady=pady)
        self.status_label.grid_remove()

        tabs_settings = tk.Frame(tabs)
        tabs.add(tabs_settings, text="Settings")

        credits_btn = tk.Button(
            tabs_settings,
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
        credits_btn.grid(row=0, column=0, padx=padx, pady=pady)

        quit_btn = tk.Button(self, text="Quit", command=self.master.destroy)
        quit_btn.grid(row=1, column=0, padx=padx, pady=pady, sticky="NW")

        self.grid()

    def on_game_update(self):
        text = ""

        if self.game.check and not self.game.checkmate:
            text += "Check. "

        if self.game.white_to_move:
            text += "White to move."
        else:
            text += "Black to move."

        if self.game.checkmate:
            text = "Checkmate."
            if not self.game.white_to_move:
                text += " White wins."
            else:
                text += " Black wins."
        elif self.game.stalemate:
            text = "Stalemate. Draw."

        self.status_label["text"] = text

    def start_game(self):
        if not hasattr(self, "game"):
            self.game = Game(self.on_game_update)
            self.board_dimension = self.game.board.width * self.board_tile_width
            self.board_window = tk.Toplevel(master=self)
            x = self.master.winfo_x() - self.board_dimension - 4
            y = self.master.winfo_y()
            self.board_window.geometry(
                "%dx%d+%d+%d" % (self.board_dimension, self.board_dimension, x, y)
            )
            self.board_window.resizable(False, False)
            self.board_frame = BoardFrame(
                self.board_window, game=self.game, tile_width=self.board_tile_width
            )
            self.master.bind("<Configure>", self.board_window_follow)
            self.board_window.protocol("WM_DELETE_WINDOW", self.on_board_window_close)

            self.start_btn.grid_remove()
            self.status_label.grid()
            self.on_game_update()

    def board_window_follow(self, event=None):
        x = self.master.winfo_x() - self.board_dimension - 4
        y = self.master.winfo_y()
        self.board_window.geometry("+%d+%d" % (x, y))

    def on_board_window_close(self):
        delattr(self, "game")
        self.master.unbind("<Configure>")
        self.board_window.destroy()
        self.start_btn.grid()
        self.status_label.grid_remove()
