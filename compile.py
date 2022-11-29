import sys
from output import output


class Compile:
    def __init__(self, get):
        sys.stdout.write = output
        self.dontcheck = {}

        self.input = get
        if self.input.strip() == "":
            print("your code is empty...")
        else:
            #self.replace()
            self.do()

    def replace(self):
        repl = {"define a function ": "def", "create a function ": "def", "make a function ": "def", "called ": " ", "with the name ": " ", ", that accept no arguments": "()", ", that accept zero arguments": "()", "prints": "print", "the value of variable": ""}
        inp = str(self.input)
        for key, value in repl.items():
            inp = inp.replace(str(key), str(value))

        numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "vourteen", "fiveteen", "sixteen", "seventeen", "eightteen", "nineteen", "tweny", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]

        for i in numbers:
            startstmt = inp.find(", that accept " + i + " arguments:")
            startops = startstmt + len(", that accept " + i + " arguments:")
            end = inp.find(".", startops)
            opsomming = inp[startops:end]
            inp = inp.replace(inp[startstmt:end], "(" + opsomming + ")")

        inp = inp.replace(", that", "")

        self.input = inp

    def do(self):
        print(self.input)
