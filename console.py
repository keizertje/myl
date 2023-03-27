from tkinter import *
from tkinter import ttk
import execute


class Console(Frame):
    border = {}
    common_entry_arguments = {}
    common_text_arguments = {}

    def __init__(self):
        """console for seeing output a. o. First, you must set the master attribute!"""
        super(Console, self).__init__()

        self.btns_frame = Frame(self, **self.border)
        self.btns_clear = ttk.Button(self.btns_frame, text="erase", command=lambda: self.erase())
        self.output = Text(self, **self.common_text_arguments, state="disabled", height=10)
        self.vscroll = Scrollbar(self, orient="vertical", command=self.output.yview)
        self.hscroll = Scrollbar(self, orient="horizontal", command=self.output.xview)
        self.output["yscrollcommand"] = self.vscroll.set
        self.output["xscrollcommand"] = self.hscroll.set
        self.input = Entry(self, **self.common_entry_arguments)

        self.input.pack(side=BOTTOM, fill=X)
        self.hscroll.pack(side=BOTTOM, fill=X)
        self.btns_frame.pack(side=LEFT, fill=Y)
        self.btns_clear.pack(pady=5)
        self.output.pack(side=LEFT, fill=BOTH, expand=True)
        self.vscroll.pack(side=LEFT, fill=Y)

        self.input.bind("<Return>", lambda e: self.stdin())

    def stdin(self):
        self.stdout(self.input.get() + "\n")
        execute.stdin(self.input.get() + "\n")
        self.input.delete("0", END)

    def stdout(self, chars):
        self.output.config(state="normal")
        self.output.insert(END + "-1c", chars)
        self.output.config(state="disabled")

    def stderr(self, chars):
        pass

    def erase(self):
        self.output.delete("1.0", END)
