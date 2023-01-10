import traceback
import sys
from output import output, set_last
from files import openfile
from alert import alert


class Execute:
    def __init__(self, name):
        self.input = openfile(name)[0]
        self.compile()

    def compile(self):
        if "tkinter" in self.input:
            if alert("This IDE is made with tkinter, do all your widgets have a master specified?", button_a_msg="yes", button_b_msg="no") == "yes":
                self.do()
        else:
            self.do()

    def do(self):
        sys.stdout.write = output
        try:
            set_last("")
            exec(self.input)
        except Exception:
            set_last("text.config(foreground='red')")
            error = traceback.format_exc()
            output(error)
