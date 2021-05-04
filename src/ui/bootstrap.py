from os import path
import tkinter as tk

from db.init import db_session
from .main import MainFrame


def bootstrap():
    root = tk.Tk()

    root.title("Chess")
    root.iconphoto(
        root._w,
        tk.PhotoImage(
            file=path.dirname(path.realpath(__file__)) + "/../img/pieces/knight_b.png"
        ),
    )

    main = MainFrame(master=root, db_session=db_session)
    main.mainloop()
