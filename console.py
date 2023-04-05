from tkinter import *
from tkinter import ttk
import subprocess as sp
import files


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

    def __init__(self):
        """console for seeing output a. o. First, you have to set the master attribute!"""
        super(Console, self).__init__()

        self.btns_frame = Frame(self, **self.border)
        self.btns_clear = ttk.Button(self.btns_frame, text="erase", command=lambda: self.master.del_cons())
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
        self.process.communicate(input=self.input.get() + "\n")
        self.input.delete("0", END)

    def stdout(self, chars: str) -> None:
        self.output.config(state="normal")
        print(chars)
        self.output.config("1.0", END + "-1c", chars)
        self.output.config(state="disabled")

    def stderr(self, chars):
        self.stdout(chars)

    def erase(self):
        print("erase is called")
        self.output.delete("1.0", END)

    def run(self, name):
        print(f"run is called. name={name}")
        if self.process is not None:
            self.process.kill()
            self.process = None
        while True:
            if self.process is None:
                self.process = sp.Popen(["C:/Users/Gebruiker/AppData/Local/Programs/Python/Python39/python.exe", files.userdir + "/python files/" + name + ".py"],
                                        stdout=open("stdout.txt", "w"),
                                        stderr=open("stderr.txt", "w"),
                                        stdin=sp.PIPE,
                                        text=True)
                self.last_stdout_length = 0
                self.last_stderr_length = 0
            if self.process is not None:
                if self.process.poll() is None:
                    # self.out, self.err = (self.process.stdout.readlines()[-1], self.process.stderr.readlines()[-1])
                    # print(self.out)
                    # # err = stderr[1].read()
                    # self.new_stdout = self.out[self.last_stdout_length:]
                    # # new_stderr = err[last_stderr_length:]
                    # self.last_stdout_length = len(self.out)
                    # # last_stderr_length = len(err)
                    # self.stdout(self.new_stdout)
                    # # master.ins_cons(new_stderr, err=True)
                    with open("stdout.txt") as f:
                        self.stdout(f.read())
                else:
                    break
        self.stdout(f"Process finished with exit code {self.process.poll()}\n")
        self.last_stdout_length = 0
        self.last_stderr_length = 0
