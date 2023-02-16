"""this is a short script to output some text in a tkinter toplevel window."""
from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
last = ""
master = None
root = None


def set_last(text):
    global last
    last = text


def output(a):
    global last
    global master
    global root
    if root is not None:
        root.destroy()
    root = Toplevel(master)
    root.geometry(f"420x400+{root.winfo_screenwidth() - 411}+{root.winfo_screenheight() - 456}")
    text = ScrolledText(root)
    text.pack(expand=True, fill="both")
    text.insert("insert", a)
    exec(last)
