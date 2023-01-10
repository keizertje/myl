from tkinter import Tk, Button
from customtext import CustomText
from execute import Execute
from coloring import color
import keyboard


class App(Tk):
    def __init__(self):
        super(App, self).__init__()

        self.width = self.winfo_screenwidth() - 1
        self.height = self.winfo_screenheight() - 1
        self.attributes('-fullscreen', True)

        self.input = CustomText(self)
        self.input.place(x=10, y=10, width=self.width - 20, height=self.height - 20)
        self.input.bind("<<TextModified>>", lambda a: color(self.input))

        self.run = Button(self, text="run", command=lambda: Execute(self.input.get("1.0", "end")))
        self.run.place(x=self.width - 20 - 50, y=20, width=50, height=30)

        self.exit = Button(self, text="exit", command=lambda: self.quit())
        self.exit.place(x=self.width - 10 - 20 - 50 - 50, y=20, width=50, height=30)

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    keyboard.add_hotkey("ctrl+enter", Execute, args=(app.input.get("1.0", "end")))
    app.start()
