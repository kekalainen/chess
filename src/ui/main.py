import tkinter as tk
import tkinter.messagebox
from tkinter.ttk import Notebook, Combobox
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, simpledialog
from platform import system
from playsound import playsound
import threading
import os
import re

from .board import BoardFrame
from game.game import Game
from db.models import Game as GameModel, Setting as SettingModel


class MainFrame(tk.Frame):
    def __init__(self, master=None, db_session=None):
        super().__init__(master)
        self.master = master
        self.db_session = db_session

        self.board_tile_width = 100

        x = self.master.winfo_screenwidth() // 2 - 150
        y = self.master.winfo_screenheight() // 2 - 50
        self.master.geometry("%dx%d+%d+%d" % (300, 275, x, y))
        self.master.resizable(False, False)

        padx = 10
        pady = 5

        self.tabs = Notebook(self)
        self.tabs.grid(row=0, column=0, sticky="NW")

        self.tabs_game = tk.Frame(self.tabs)
        self.tabs.add(self.tabs_game, text="Game")

        self.start_frame = tk.Frame(self.tabs_game)
        self.start_frame.grid(row=0, column=0, pady=pady, sticky="NW")
        self.start_btn = tk.Button(
            self.start_frame, text="Play", command=self.start_game
        )
        self.start_btn.grid(row=0, column=0, padx=padx, pady=pady, sticky="NW")
        self.ai_difficulty = tk.IntVar(self, -1)
        for ai_difficulty in [((0, 0), "2 players", -1), ((1, 0), "Random AI", 0), ((0, 1), "Normal AI", 1)]:
            radio_btn = tk.Radiobutton(
                self.start_frame,
                variable=self.ai_difficulty,
                text=ai_difficulty[1],
                val=ai_difficulty[2],
            )
            radio_btn.grid(row=ai_difficulty[0][1], column=ai_difficulty[0][0] + 1, pady=pady, sticky="NW")

        self.status_frame = tk.Frame(self.tabs_game)
        self.status_frame.grid(row=1, column=0, padx=padx, pady=pady, sticky="NW")
        self.status_frame.grid_remove()

        self.status_label = tk.Label(self.status_frame, text="")
        self.status_label.grid(row=0, column=0, pady=pady, sticky="NW")

        self.draw_btn = tk.Button(
            self.status_frame, text="Claim draw", command=self.claim_draw
        )
        self.draw_btn.grid(row=0, column=1, padx=padx, pady=pady, sticky="NE")
        self.draw_btn.grid_remove()

        self.moves_text = ScrolledText(
            self.status_frame, width=20, height=3, state=tk.DISABLED
        )
        self.moves_text.grid(row=1, column=0, pady=pady)

        self.promotion_piece = tk.StringVar(self, "Q")
        self.promotion_piece_selection_frame = tk.Frame(self.tabs_game)
        self.promotion_piece_selection_frame.grid(row=3, column=0, padx=padx, pady=pady)
        self.promotion_piece_selection_frame.grid_remove()
        promotion_label = tk.Label(
            self.promotion_piece_selection_frame, text="Promotion piece"
        )
        promotion_label.grid(row=0, column=0, sticky="NW")
        for promotion_piece in [
            (0, "Knight", "N"),
            (1, "Bishop", "B"),
            (2, "Rook", "R"),
            (3, "Queen", "Q"),
        ]:
            radio_btn = tk.Radiobutton(
                self.promotion_piece_selection_frame,
                variable=self.promotion_piece,
                command=self.on_promotion_piece_selected,
                text=promotion_piece[1],
                val=promotion_piece[2],
            )
            radio_btn.grid(row=1, column=promotion_piece[0], pady=pady)

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

        self.save_game_btn = tk.Button(
            self.tabs_game, text="Save", command=self.db_save_game
        )
        self.save_game_btn.grid(row=4, column=0, padx=padx, pady=pady, sticky="NW")
        self.save_game_btn.grid_remove()

        self.tabs_database = tk.Frame(self.tabs)
        self.tabs.add(self.tabs_database, text="Database")

        self.pgn_label = tk.Label(self.tabs_database, text="Portable Game Notation")
        self.pgn_label.grid(row=0, column=0, padx=padx, sticky="NW")

        self.pgn_text = ScrolledText(self.tabs_database, width=20, height=3)
        self.pgn_text.grid(row=1, column=0, padx=padx, pady=pady, sticky="NW")

        pgn_btn_frame = tk.Frame(self.tabs_database)
        pgn_btn_frame.grid(row=2, column=0, pady=pady, sticky="NW")

        import_btn = tk.Button(pgn_btn_frame, text="Import", command=self.import_pgn)
        import_btn.grid(row=0, column=0, padx=padx, pady=pady)

        export_btn = tk.Button(pgn_btn_frame, text="Export", command=self.export_pgn)
        export_btn.grid(row=0, column=1, padx=padx, pady=pady)

        view_btn = tk.Button(
            pgn_btn_frame, text="View", command=lambda: self.start_game(view_mode=True)
        )
        view_btn.grid(row=0, column=2, padx=padx, pady=pady)

        game_list_frame = tk.Frame(self.tabs_database)
        game_list_frame.grid(row=4, column=0, pady=pady)

        game_list_label = tk.Label(game_list_frame, text="Stored games")
        game_list_label.grid(row=0, column=0, padx=padx, sticky="NW")

        self.game_combobox = Combobox(game_list_frame, state="readonly")
        self.game_combobox.grid(row=1, column=0, padx=padx, pady=pady)

        load_btn = tk.Button(game_list_frame, text="Load", command=self.db_load_pgn)
        load_btn.grid(row=1, column=1, padx=padx, pady=pady)

        delete_btn = tk.Button(
            game_list_frame, text="Delete", command=self.db_delete_game
        )
        delete_btn.grid(row=1, column=2, padx=padx, pady=pady)

        self.db_load_games()

        self.tabs_settings = tk.Frame(self.tabs)
        self.tabs.add(self.tabs_settings, text="Settings")

        self.enable_sounds = tk.BooleanVar(
            value=self.db_get_setting("enable_sounds", "0") == "1"
        )
        if system() != "Linux":
            sound_checkbtn = tk.Checkbutton(
                self.tabs_settings,
                text="Enable sounds",
                variable=self.enable_sounds,
                command=lambda: self.db_store_setting(
                    "enable_sounds", "1" if self.enable_sounds.get() else "0"
                ),
            )
            sound_checkbtn.grid(row=0, column=0, padx=padx, pady=pady, sticky="NW")

        self.theme = tk.StringVar(self, self.db_get_setting("theme", "Classic"))

        theme_frame = tk.Frame(self.tabs_settings)
        theme_frame.grid(row=1, column=0, pady=pady)

        theme_label = tk.Label(theme_frame, text="Theme")
        theme_label.grid(row=0, column=0, padx=padx, sticky="NW")
        theme_combobox = Combobox(
            theme_frame,
            textvariable=self.theme,
            values=["Classic", "Dark"],
            state="readonly",
        )
        theme_combobox.bind("<<ComboboxSelected>>", self.update_theme)
        theme_combobox.grid(row=1, column=0, padx=padx, pady=pady)

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
        credits_btn.grid(row=2, column=0, padx=padx, pady=pady, sticky="NW")

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

    def db_save_game(self):
        name = simpledialog.askstring(
            "Save PGN", "Enter a name for the game.", parent=self
        )
        if name:
            game = GameModel(name=name, pgn=self.moves_text.get(1.0, tk.END))
            self.db_session.add(game)
            self.db_session.commit()
            self.db_load_games()

    def db_load_games(self):
        self.db_games = (
            self.db_session.query(GameModel).order_by(GameModel.id.desc()).all()
        )
        names = []
        for game in self.db_games:
            names.append(game.name)
        self.game_combobox.config(values=names)
        if names:
            self.game_combobox.set(names[0])
        else:
            self.game_combobox.set("")

    def db_load_pgn(self):
        if len(self.db_games) > 0:
            game = self.db_games[self.game_combobox.current()]
            self.pgn_text.delete(1.0, tk.END)
            self.pgn_text.insert(1.0, game.pgn)

    def db_delete_game(self):
        if len(self.db_games) > 0:
            game = self.db_games[self.game_combobox.current()]
            self.db_session.delete(game)
            self.db_session.commit()
            self.db_load_games()

    def db_get_setting(self, name, fallback):
        setting = (
            self.db_session.query(SettingModel)
            .filter(SettingModel.name == name)
            .first()
        )
        if setting:
            return setting.value
        return fallback

    def db_store_setting(self, name, value):
        setting = (
            self.db_session.query(SettingModel)
            .filter(SettingModel.name == name)
            .first()
        )
        if setting:
            setting.value = value
        else:
            setting = SettingModel(name=name, value=str(value))
        self.db_session.add(setting)
        self.db_session.commit()

    def play_move_sound(self, undo=False):
        """Plays a sound for a moving piece."""
        threading.Thread(
            target=playsound,
            args=(
                "src/audio/move_"
                + (
                    "2"
                    if (undo and not self.game.white_to_move)
                    or (not undo and self.game.white_to_move)
                    else "1"
                )
                + ".mp3",
            ),
            daemon=True,
        ).start()

    def update_theme(self, event=None):
        """Stores the selected theme and updates the board, if necessary."""
        theme = self.theme.get()
        self.db_store_setting("theme", theme)
        if hasattr(self, "game"):
            colors = ["#542E1D", "#EFD8B0"]
            if theme == "Dark":
                colors = ["#9C9C9C", "#4A4A4A"]
            self.board_frame.tile_colors = colors
            self.board_frame.draw_board()

    def on_game_update(self):
        game_over_previously = "to move" not in self.status_label["text"]
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
        elif self.game.draw:
            text = "Draw."

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

        if self.game.checkmate or self.game.stalemate or self.game.draw:
            move_log = move_log[0 : len(move_log) - 1] + " "
            if self.game.checkmate:
                if self.game.white_to_move:
                    move_log += "0-1"
                else:
                    move_log += "1-0"
            else:
                move_log += "1/2-1/2"

        self.moves_text.config(state=tk.NORMAL)
        self.moves_text.delete(1.0, tk.END)
        self.moves_text.insert(1.0, move_log)
        self.moves_text.config(state=tk.DISABLED)
        self.moves_text.yview(tk.END)

        if not self.game.draw and True in self.game.can_claim_draw:
            self.draw_btn.grid()
        else:
            self.draw_btn.grid_remove()

        if hasattr(self.game, "ai") and self.game.white_to_move:
            self.board_frame.draw_pieces()

        moves_length = len(self.game.an_moves)
        if self.enable_sounds.get() and self.previous_moves_length != moves_length:
            undo = self.previous_moves_length > moves_length
            if hasattr(self.game, "ai") and undo and not game_over_previously:
                self.play_move_sound(not undo)
            self.play_move_sound(undo)
            self.previous_moves_length = moves_length

    def on_promotion_piece_selected(self):
        if hasattr(self, "game"):
            self.game.board.promotion_piece = self.promotion_piece.get()

    def start_game(self, view_mode=False):
        if not hasattr(self, "game"):
            self.previous_moves_length = 0
            if view_mode:
                self.active_pgn = re.findall(
                    "((?!-)[a-zA-Z0-]+[0-9]?\w+=?[N|B|R|Q]?)(?![^{]*})(?![^[]*])",
                    self.pgn_text.get(1.0, tk.END),
                )
                if not self.active_pgn:
                    return
                self.active_pgn_index = 0
                self.previous_move_btn.configure(state=tk.DISABLED)
                self.next_move_btn.configure(state=tk.NORMAL)
                self.view_control_btn_frame.grid()
                self.tabs.select(self.tabs_game)
            else:
                self.promotion_piece_selection_frame.grid()
                self.save_game_btn.grid()

            self.game = Game(
                on_update=self.on_game_update,
                ai_difficulty=self.ai_difficulty.get() if not view_mode else -1,
            )
            self.game.board.promotion_piece = self.promotion_piece.get()
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
            self.update_theme()
            self.master.bind("<Configure>", self.board_window_follow)
            self.board_window.protocol("WM_DELETE_WINDOW", self.on_board_window_close)

            self.start_frame.grid_remove()
            self.status_frame.grid()
            self.on_game_update()

    def claim_draw(self):
        if hasattr(self, "game"):
            if self.game.claim_draw():
                self.board_frame.deselect_tile()
                self.draw_btn.grid_remove()

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
        self.start_frame.grid()
        self.status_frame.grid_remove()
        self.view_control_btn_frame.grid_remove()
        self.promotion_piece_selection_frame.grid_remove()
        self.save_game_btn.grid_remove()
        self.draw_btn.grid_remove()
