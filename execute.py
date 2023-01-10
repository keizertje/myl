import sys
from output import output


class Execute:
    def __init__(self, get):
        sys.stdout.write = output

        self.input = get
        if self.input.strip() == "":
            print("your code is empty...")
        else:
            self.compile()
            self.do()

    def compile(self):
        pass

    def do(self):
        try:
            exec(self.input)
        except Exception as msg:
            output(msg, "text.config(foreground='red')")
        else:
            output("no errors, good job!", "")
        finally:
            pass
