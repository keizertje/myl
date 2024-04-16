from tkinter import *
from tkinter import ttk
import files
from execute import Execute


class Console(Frame):
    border = {}
    common_entry_arguments = {}
    common_text_arguments = {}
    process = None
    out = ""
    err = ""
    last_stdout_length = 0
    last_stderr_length = 0
    new_stdout = ""
    new_stderr = ""

    def __init__(self, **kwargs):
        """console for seeing output a. o. You have to set the master attribute!"""
        super(Console, self).__init__()
        
        for k, v in kwargs.items():
            self.__setattr__(k, v)

        self.executer = Execute(self)

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

        self.input.bind("<Return>", lambda e: self.handle_input())

    def write(self, __s):
        self.output["state"] = "normal"
        self.output.insert(END, __s)
        self.output["state"] = "disabled"

    def erase(self):
        self.output["state"] = "normal"
        self.output.delete("1.0", END)
        self.output["state"] = "disabled"

    def handle_input(self):
        if self.executer.is_running:
            text = self.input.get()
            self.input.delete(0, END)
            self.write(text + "\n")

            self.executer.send_input(text + "\n")

    def run(self, name: str):
        self.executer.start("python \"" + files.pythonfilesdir + name + ".py\"")
