import tkinter as tk
from tkinter import ttk
from compile import Compile
import keyboard


class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()

        self.width = self.winfo_screenwidth() - 1
        self.height = self.winfo_screenheight() - 1
        self.attributes('-fullscreen', True)

        self.input = tk.Text(self)
        self.input.place(x=10, y=10, width=self.width - 20, height=self.height - 20)

        self.run = tk.Button(self, text="run", command=lambda: Compile(self.input.get("1.0", "end")))
        self.run.place(x=self.width - 20 - 50, y=20, width=50, height=30)

        self.exit = tk.Button(self, text="exit", command=lambda: self.quit())
        self.exit.place(x=self.width - 10 - 20 - 50 - 50, y=20, width=50, height=30)

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    keyboard.add_hotkey("ctrl+enter", Compile, args=(app.input.get("1.0", "end")))
    app.start()
