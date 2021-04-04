from os import path
import tkinter as tk

from .main import MainFrame


def bootstrap():
    root = tk.Tk()

    root.title("Chess")
    root.iconphoto(
        root._w,
        tk.PhotoImage(
            file=path.dirname(path.realpath(__file__)) + "/../img/pieces/pawn_b.png"
        ),
    )

    main = MainFrame(master=root)
    main.mainloop()
