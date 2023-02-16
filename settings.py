import tkinter as tk
from tkinter.filedialog import askdirectory
import files
import output

master = None

settings = files.openfile("")


def choosedir():
    chosen = askdirectory(initialdir="c://users")
    files.userdir = f"{chosen}"
    output.output(files.userdir)


def opensettings():
    global master
    root = tk.Toplevel(master)
    root.geometry("700x750")
