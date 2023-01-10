"""this is a script to alert a message in a tkinter window."""
from tkinter import Toplevel, Entry, Button, IntVar, StringVar, Frame
root = None
master = None


def set_master(new_master):
    global master
    master = new_master


def alert(msg: str, choice=True, button_a_msg: str = "Ok", button_b_msg: str = "cancel"):
    global root
    global master
    try:
        if root is not None:
            root.destroy()
        root = Toplevel(master)
        root.geometry("275x40")
        text = Entry(root)
        text.insert("0", msg)
        text.pack(expand=True, fill="x")
        clicked = IntVar(root)
        clicked.set(0)
        chosen = StringVar(root)
        if choice:
            button_a = Button(root, text=button_a_msg, command=lambda: [clicked.set(1), chosen.set(button_a_msg)])
            button_b = Button(root, text=button_b_msg, command=lambda: [clicked.set(1), chosen.set(button_b_msg)])
            button_a.pack(side="left", expand=True, fill="x")
            button_b.pack(side="right", expand=True, fill="x")
        else:
            button_a = Button(root, text=button_a_msg, command=lambda: [clicked.set(1), chosen.set(button_a_msg)])
            button_a.pack()
        text.config(state="disabled")
        button_a.wait_variable(clicked)
        result = chosen.get()
        root.destroy()
        return result
    except Exception as e:
        print(e)
