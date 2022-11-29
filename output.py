from tkinter import Toplevel, Label


def output(a):
    root = Toplevel()
    root.geometry(f"300x400+{root.winfo_screenwidth() - 331}+{root.winfo_screenheight() - 456}")
    text = Label(root, anchor="nw", text=a)
    text.pack(expand=True, fill="both")
