"""this is a short script to output some text in a tkinter toplevel window."""
from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
last = ""
master = None
root = None


def set_last(text):
    global last
    last = text


def set_master(new_master):
    global master
    master = new_master


def output(a):
    global master
    global root
    if root is not None:
        root.destroy()
    global last
    root = Toplevel(master)
    root.geometry(f"420x400+{root.winfo_screenwidth() - 431}+{root.winfo_screenheight() - 456}")
    text = ScrolledText(root)
    text.insert("end-1c", a)
    text.config(state="disabled", background="#eee")
    text.pack(expand=True, fill="both")
    exec(last)
