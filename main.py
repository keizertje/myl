from tkinter import *
from tkinter.filedialog import askopenfilename
from versions import VersionManager  # self-made
from coloring import color  # self-made
import execute  # self-made
import alert  # self-made
import output  # self-made
import files  # self-made
import settings  # self-made


# TODO -fix ctrl+z
# TODO -fix levels

class App(Tk):
    def __init__(self):
        super(App, self).__init__()
        output.set_master(self); alert.set_master(self); files.set_master(self); settings.set_master(self)

        self.attributes('-fullscreen', True)

        self.state = StringVar(self, value="saved")
        self.newfile = StringVar(self, value="new")
        self.file = StringVar(self)
        self.lastsavedtext = StringVar(self)
        self.changes = VersionManager()
        self.filename = StringVar(self, value="Untitled (saved)")
        self.levels = [0]

        self.state.trace_add("write", callback=lambda a, b, c: self.filename.set(("Untitled" if self.file.get().strip() == "" else self.file.get()) + (" (" + self.state.get() + ")")))
        self.file.trace_add("write", callback=lambda a, b, c: [self.set_input(files.openfile(self.file.get())[0]), self.name.delete("0", END), self.name.insert(END, self.file.get().split(".")[0]), self.filename.set(("Untitled " if self.file.get().strip() == "" else self.file.get()) + "(" + self.state.get() + ")")])

        self.header = Label(self, textvariable=self.filename, font='Arial 18')
        self.input = Text(self, font='Arial 11', selectbackground="#acf", selectforeground="#000")
        self.run = Button(self, text="run", command=lambda: [files.create(self.name.get(), self.get_input()) if self.state.get() == "unsaved" and self.newfile.get() == "old" else None, execute.Execute(self.name.get())])
        self.exit = Button(self, text="exit", command=lambda: [(files.create(self.name.get(), self.get_input()) if self.state.get() == "unsaved" and self.newfile.get() == "old" else None), self.quit()])
        self.save = Button(self, text="save", command=lambda: self.savefile())
        self.open = Button(self, text="open", command=lambda: self.openfile())
        self.settings = Button(self, text="settings", command=lambda: settings.opensettings())
        self.name = Entry(self, border=3, font=('Arial', 13))
        self.bottom = Frame(self)
        self.indexer = Label(self.bottom, text="1:1")

        self.bottom.pack(side=BOTTOM, padx=5, pady=5, fill=X)
        self.indexer.pack(side=RIGHT, padx=5)
        self.input.pack(side=BOTTOM, expand=True, fill=BOTH, padx=10)
        self.header.pack(side=LEFT, padx=10, pady=5)
        self.exit.pack(side=RIGHT, padx=5, ipadx=10)
        self.run.pack(side=RIGHT, padx=5, ipadx=10)
        self.save.pack(side=RIGHT, padx=5, ipadx=10)
        self.open.pack(side=RIGHT, padx=5, ipadx=10)
        self.settings.pack(side=RIGHT, padx=5, ipadx=10)
        self.name.pack(side=RIGHT, padx=5, ipadx=20)

        self.input.bind("<KeyRelease>", lambda e: self.afterKeyPress(e))
        self.input.bind("<Key>", lambda e: self.onKeyPress(e))
        self.input.bind("<Control-Enter>", lambda e: [self.set_input(self.get_input() + "\b"), self.run.invoke()])
        self.input.bind("<Escape>", lambda e: self.exit.invoke())
        self.input.bind("<Control-s>", lambda e: self.save.invoke())
        self.input.bind("<Control-o>", lambda e: self.open.invoke())
        self.input.bind("<Control-z>", lambda e: [self.changes.change_version(-1), self.set_input(self.changes.current())])
        self.input.bind("<Control-y>", lambda e: [self.changes.change_version(1), self.set_input(self.changes.current())])

        self.input.focus()
        self.loop()

    def openfile(self):
        if self.state.get() == "unsaved":
            choise = alert.alert("your code is unsaved, save now?")
            if choise == "Ok":
                files.create(self.name.get(), self.get_input())
        chosen = askopenfilename(filetypes=[("Python Files", ".py")], initialdir=files.userdir + "/python files").split("/")[-1].split(".")[0]
        self.file.set(chosen)
        if files.openfile(chosen)[1]:
            self.state.set("saved")
            self.newfile.set("old")
            self.lastsavedtext.set(self.get_input())
        else:
            self.file.set("")
            self.state.set("unsaved")
        self.afterKeyPress()

    def set_input(self, content):
        self.input.delete("1.0", END)
        self.input.insert(END, content)

    def get_input(self):
        return self.input.get("1.0", END + "-1c")

    def onKeyPress(self, e=None):
        if e is not None:
            if e.keysym == "Up" and self.input.index(INSERT).split(".")[0] == "1":
                self.input.mark_set(INSERT, "1.0")
            if e.keysym == "Down" and self.input.index(INSERT).split(".")[0] == self.input.index(END+"-1c").split(".")[0]:
                self.input.mark_set(INSERT, END+"-1c")

    def afterKeyPress(self, e=None):
        if e is not None:
            if e.keysym == "Tab":
                self.input.delete(INSERT + "-1c", INSERT)
                self.input.insert(INSERT, "    ")
        color(self.input)
        index = self.input.index(INSERT).split(".")
        index[1] = str(int(index[1])+1)
        self.indexer.config(text=":".join(index))
        self.state.set("saved" if self.lastsavedtext.get() == self.get_input() else "unsaved")
        self.changes.add_version(self.get_input())

    def savefile(self):
        files.create(self.name.get(), self.get_input())
        self.lastsavedtext.set(self.get_input())
        self.afterKeyPress()

    def loop(self):
        self.onKeyPress()
        self.afterKeyPress()
        self.after(10, lambda: self.loop())


if __name__ == "__main__":
    app = App()
    app.mainloop()
