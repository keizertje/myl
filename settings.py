import tkinter as tk
from tkinter.filedialog import askdirectory
import files
import output

master = None

settings = files.openfile("")


def opensettings():
    global master
    root = tk.Toplevel(master)
    root.geometry("700x750")
