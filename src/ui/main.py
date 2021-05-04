import tkinter as tk
import tkinter.messagebox
from tkinter.ttk import Notebook
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import os
import re

from .board import BoardFrame
from game.game import Game


class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.board_tile_width = 100

        x = self.master.winfo_screenwidth() // 2 - 150
        y = self.master.winfo_screenheight() // 2 - 50
        self.master.geometry("%dx%d+%d+%d" % (300, 225, x, y))
        self.master.resizable(False, False)

        padx = 10
        pady = 5

        self.tabs = Notebook(self)
        self.tabs.grid(row=0, column=0, sticky="NW")

        self.tabs_game = tk.Frame(self.tabs)
        self.tabs.add(self.tabs_game, text="Game")

        self.start_btn = tk.Button(self.tabs_game, text="Play", command=self.start_game)
        self.start_btn.grid(row=0, column=0, padx=padx, pady=pady)

        self.status_frame = tk.Frame(self.tabs_game)
        self.status_frame.grid(row=1, column=0, padx=padx, pady=pady)
        self.status_frame.grid_remove()

        self.status_label = tk.Label(self.status_frame, text="")
        self.status_label.grid(row=0, column=0, pady=pady, sticky="NW")

        self.moves_text = ScrolledText(
            self.status_frame, width=20, height=3, state=tk.DISABLED
        )
        self.moves_text.grid(row=1, column=0, pady=pady)

        self.view_control_btn_frame = tk.Frame(self.tabs_game)
        self.view_control_btn_frame.grid(row=3, column=0, padx=padx, pady=pady)
        self.view_control_btn_frame.grid_remove()

        self.previous_move_btn = tk.Button(
            self.view_control_btn_frame, text="Previous", command=self.previous_move
        )
        self.previous_move_btn.grid(row=0, column=0, padx=padx, pady=pady)

        self.next_move_btn = tk.Button(
            self.view_control_btn_frame, text="Next", command=self.next_move
        )
        self.next_move_btn.grid(row=0, column=1, padx=padx, pady=pady)

        self.tabs_database = tk.Frame(self.tabs)
        self.tabs.add(self.tabs_database, text="Database")

        self.pgn_label = tk.Label(self.tabs_database, text="Portable Game Notation")
        self.pgn_label.grid(row=0, column=0, padx=padx, sticky="NW")

        self.pgn_text = ScrolledText(self.tabs_database, width=20, height=3)
        self.pgn_text.grid(row=1, column=0, padx=padx, pady=pady)

        pgn_btn_frame = tk.Frame(self.tabs_database)
        pgn_btn_frame.grid(row=2, column=0, padx=padx, pady=pady)

        import_btn = tk.Button(pgn_btn_frame, text="Import", command=self.import_pgn)
        import_btn.grid(row=0, column=0, padx=padx, pady=pady)

        export_btn = tk.Button(pgn_btn_frame, text="Export", command=self.export_pgn)
        export_btn.grid(row=0, column=1, padx=padx, pady=pady)

        view_btn = tk.Button(
            pgn_btn_frame, text="View", command=lambda: self.start_game(view_mode=True)
        )
        view_btn.grid(row=0, column=2, padx=padx, pady=pady)

        self.tabs_settings = tk.Frame(self.tabs)
        self.tabs.add(self.tabs_settings, text="Settings")

        credits_btn = tk.Button(
            self.tabs_settings,
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

    def import_pgn(self):
        path = filedialog.askopenfilename(
            title="Import a PGN file",
            filetypes=[("PGN file", "*.pgn")],
        )
        if path:
            with open(path) as f:
                self.pgn_text.delete(1.0, tk.END)
                self.pgn_text.insert(1.0, f.read())

    def export_pgn(self):
        path = filedialog.asksaveasfilename(
            title="Export a PGN file",
            filetypes=[("PGN file", "*.pgn")],
            defaultextension=".pgn",
        )
        if path:
            with open(path, "w") as f:
                f.write(self.pgn_text.get(1.0, tk.END))

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

        move_log = ""
        for i in range(len(self.game.an_moves)):
            if i % 2 == 0:
                move_log += str(i // 2 + 1) + ". "
            move_log += self.game.an_moves[i]
            if i % 2 == 0:
                move_log += " "
            else:
                move_log += "\n"

        self.moves_text.config(state=tk.NORMAL)
        self.moves_text.delete(1.0, tk.END)
        self.moves_text.insert(1.0, move_log)
        self.moves_text.config(state=tk.DISABLED)
        self.moves_text.yview(tk.END)

    def start_game(self, view_mode=False):
        if not hasattr(self, "game"):
            if view_mode:
                self.active_pgn = re.findall(
                    "([a-zA-Z]+[0-9]?\w+)(?![^{]*})(?![^[]*])",
                    self.pgn_text.get(1.0, tk.END),
                )
                if not self.active_pgn:
                    return
                self.active_pgn_index = 0
                self.previous_move_btn.configure(state=tk.DISABLED)
                self.next_move_btn.configure(state=tk.NORMAL)
                self.view_control_btn_frame.grid()
                self.tabs.select(self.tabs_game)

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
                self.board_window,
                game=self.game,
                tile_width=self.board_tile_width,
                view_mode=view_mode,
            )
            self.master.bind("<Configure>", self.board_window_follow)
            self.board_window.protocol("WM_DELETE_WINDOW", self.on_board_window_close)

            self.start_btn.grid_remove()
            self.status_frame.grid()
            self.on_game_update()

    def next_move(self):
        n = len(self.active_pgn)
        if self.active_pgn_index < n:
            self.game.move_piece_an(self.active_pgn[self.active_pgn_index])
            self.board_frame.draw_pieces()
            self.active_pgn_index += 1
            if self.active_pgn_index == n:
                self.next_move_btn.configure(state=tk.DISABLED)
            self.previous_move_btn.configure(state=tk.NORMAL)

    def previous_move(self):
        if self.active_pgn_index > 0:
            self.game.undo_move()
            self.board_frame.draw_pieces()
            self.active_pgn_index -= 1
            if self.active_pgn_index == 0:
                self.previous_move_btn.configure(state=tk.DISABLED)
            self.next_move_btn.configure(state=tk.NORMAL)

    def board_window_follow(self, event=None):
        x = self.master.winfo_x() - self.board_dimension - 4
        y = self.master.winfo_y()
        self.board_window.geometry("+%d+%d" % (x, y))

    def on_board_window_close(self):
        delattr(self, "game")
        self.master.unbind("<Configure>")
        self.board_window.destroy()
        self.start_btn.grid()
        self.status_frame.grid_remove()
        self.view_control_btn_frame.grid_remove()
