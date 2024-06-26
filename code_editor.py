from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as alert
from coloring import Color                      # self-made
from threading import Thread
import files                                    # self-made
import settings                                 # self-made
from console import Console


class App(Tk):
    def __init__(self):
        """ Here the app is created.
            first: the variables
            second: the widgets
            third: the packs
            last: the hotkeys"""

        # init tkinter.Tk()
        super(App, self).__init__()

        # set the global master variables in other files
        files.master = self
        settings.master = self

        # set title
        self.title("python IDE")

        # var types supported by tkinter for trace adds and non-statement variable changes
        self.state = StringVar(self, value="unsaved")
        self.newfile = StringVar(self, value="new")
        self.file = StringVar(self)
        self.lastsavedtext = StringVar(self)
        self.filename = StringVar(self, value="Untitled (unsaved)")
        self.levels = [0]
        self.border = {"highlightbackground": "#bbb", "highlightthickness": "1px", "highlightcolor": "#bbb", "relief": FLAT}
        self.common_entry_arguments = {**self.border, "font": 'arial 11', "selectbackground": "#acf", "selectforeground": "#000"}
        self.common_text_arguments = {**self.common_entry_arguments, "wrap": NONE, "tabs": "16"}
        self.open_files = {self.__get_filename(): ""}

        # automatic header updates a. o.
        self.state.trace_add("write", callback=lambda *args, **kwargs: self.filename.set(self.__get_filename()))
        self.file.trace_add("write", callback=lambda *args, **kwargs: [self.set_input(files.openfile(self.file.get())[0]),
                                                                       self.name.delete("0", END),
                                                                       self.name.insert(END, self.file.get().split(".")[0]),
                                                                       self.filename.set(self.__get_filename())])

        # creating the widgets
        # main coding
        self.input_frame = Frame(self)
        self.tab_buttons = Frame(self.input_frame, **self.border)
        self.input = Text(self.input_frame, undo=True, **self.common_text_arguments)
        self.vscroll = Scrollbar(self.input_frame, orient="vertical", command=self.input.yview)
        self.hscroll = Scrollbar(self.input_frame, orient="horizontal", command=self.input.xview)
        self.input.config(yscrollcommand=self.vscroll.set)
        self.input.config(xscrollcommand=self.hscroll.set)
        self.line_numbers = Text(self.input_frame, width=4, background="#fff", state="disabled", **self.common_text_arguments)

        # console
        self.console = Console(master=self,
                               border=self.border,
                               common_entry_arguments=self.common_entry_arguments,
                               common_text_arguments=self.common_text_arguments)

        # top frame for buttons and header.
        self.toppadding = Frame(self, height=5)
        self.top = Frame(self)
        self.header = Label(self.top, textvariable=self.filename, font='arial 18')
        self.run = ttk.Button(self.top, text="run", command=lambda: [self.savefile(),
                                                                     self.console.run(self.name.get())])
        self.exit = ttk.Button(self.top, text="exit", command=lambda: self.exit_app())
        self.save = ttk.Button(self.top, text="save", command=lambda: self.savefile())
        self.open = ttk.Button(self.top, text="open", command=lambda: self.__openfile())
        self.settings = ttk.Button(self.top, text="settings", command=lambda: settings.opensettings())
        self.name = Entry(self.top, **self.common_entry_arguments)

        # bottom info
        self.bottom = Frame(self, **self.border)
        self.indexer = Label(self.bottom, text="1:1")

        # pack anything at the right place
        # the lowest layer first
        self.bottom.pack(side=BOTTOM, padx=10, pady=5, fill=X)
        self.indexer.pack(side=RIGHT, padx=5)

        # the console
        self.console.pack(side=BOTTOM, fill=X, padx=10)

        # main coding widget
        self.input_frame.pack(side=BOTTOM, expand=True, fill=BOTH, padx=10, pady=10)
        self.tab_buttons.pack(side=TOP, fill=X)
        self.hscroll.pack(side=BOTTOM, fill=X)
        self.line_numbers.pack(side=LEFT, fill=Y)
        self.input.pack(side=LEFT, expand=True, fill=BOTH)
        self.vscroll.pack(side=LEFT, fill=Y)

        # padding at the top
        self.toppadding.pack()

        # headers and main buttons
        self.top.pack(fill=X)
        self.header.pack(side=LEFT, padx=10)
        self.exit.pack(side=RIGHT, padx=5, ipadx=10)
        self.run.pack(side=RIGHT, padx=5, ipadx=10)
        self.save.pack(side=RIGHT, padx=5, ipadx=10)
        self.open.pack(side=RIGHT, padx=5, ipadx=10)
        self.settings.pack(side=RIGHT, padx=5, ipadx=10)
        self.name.pack(side=RIGHT, padx=5, ipadx=20)

        # bindings and hotkeys
        self.input.bind("<Key>", lambda e: self.onKeyPress(e))
        self.input.bind_all("<Control-Return>", lambda e: [self.set_input(self.get_input()[:-1]), self.run.invoke()])
        self.input.bind_all("<Escape>", lambda e: self.exit.invoke())
        self.input.bind_all("<Control-s>", lambda e: self.save.invoke())
        self.input.bind_all("<Control-o>", lambda e: self.open.invoke())
        self.input.bind_all("<Control-z>", lambda e: self.input.edit_undo())
        self.input.bind_all("<Control-y>", lambda e: self.input.edit_redo())
        self.input.bind_all("<Control-n>", lambda e: App().mainloop())
        
        self.__openfile("new file")
        self.input.focus()
        self.loop()

    def exit_app(self):
        if self.state == "unsaved":
            if alert.askquestion(title="save now?", message="your code is unsaved! save now?") == alert.YES:
                self.savefile()
        self.destroy()
        self.quit()

    def __openfile(self, name=None):
        if not name:
            if self.state.get() == "unsaved" and self.newfile.get() == "old":
                if alert.askquestion(title="save now?", message="your code is unsaved! save now?") == alert.YES:
                    self.savefile()
            chosen = askopenfilename(filetypes=[("Python files", ".py"), ("All files", "")], initialdir=files.userdir + "/python files")
            chosen = chosen.split("/")[-1].split(".")[0]
        else:
            chosen = name
        self.file.set(chosen)
        if files.openfile(chosen)[1]:
            self.state.set("saved")
            self.newfile.set("old")
            self.lastsavedtext.set(self.get_input())
        else:
            self.file.set("")
            self.state.set("unsaved")
        Color(self.input)
        ttk.Button(self.tab_buttons, text=chosen, command=(lambda *a: self.file.set(chosen))).pack(side=LEFT)

    def set_input(self, content):
        self.input.delete("1.0", END)
        self.input.insert(END, content)

    def get_input(self):
        return self.input.get("1.0", END + "-1c")

    def onKeyPress(self, e=None):
        self.state.set("saved" if self.lastsavedtext.get() == self.get_input() else "unsaved")
        if e is not None:
            if e.keysym == "Up" and self.input.index(INSERT).split(".")[0] == "1":
                self.input.mark_set(INSERT, "1.0")
            if e.keysym == "Down" and self.input.index(INSERT).split(".")[0] == self.input.index(END + "-1c").split(".")[0]:
                self.input.mark_set(INSERT, END + "-1c")

    def savefile(self):
        if self.state.get() == "unsaved":
            files.create(self.name.get(), self.get_input())
            self.lastsavedtext.set(self.get_input())
        Color(self.input)

    def loop(self):
        # Colors
        Color(self.input)

        # indexer in the bottom
        index = self.input.index(INSERT).split(".")
        index[1] = str(int(index[1]) + 1)
        self.indexer.config(text=":".join(index))

        # line numbers
        self.line_numbers["state"] = "normal"
        self.line_numbers.delete("1.0", END)
        for i in range(self.input.count("1.0", END, "lines")[0]):
            str_i = str(i + 1)
            if i + 1 < 1000:
                str_i = " " + str_i
                if i + 1 < 100:
                    str_i = " " + str_i
                    if i + 1 < 10:
                        str_i = " " + str_i
            self.line_numbers.insert(END, ("\n" + str_i) if i + 1 != 1 else str_i)
        self.line_numbers.yview_moveto(self.input.yview()[0])
        self.line_numbers["state"] = "disabled"

        # recursion
        self.after(10, lambda: self.loop())

    def __get_filename(self):
        return ("Untitled " if self.file.get().strip() == "" else self.file.get()) + "(" + self.state.get() + ")"

    def ins_cons(self, chars, err=False):
        if err:
            self.console.stderr(chars)
        else:
            self.console.stdout(chars)

    def del_cons(self):
        self.console.output.config(state="normal")
        self.console.output.delete("1.0", END + "-1c")
        self.console.output.config(state="disabled")

    def search(self):
        for tag in self.input.tag_names():
            self.input.tag_delete(tag)
        inp = self.search_entry.get()
        pos = self.input.search(inp, "1.0", END)
        while pos != "":
            self.input.tag_add(pos, pos, f"{pos}+{len(inp)}c")
            self.input.tag_config(pos, background="#ed0")
            print(pos, f"{pos}+{len(inp)}c", end="\t\t")
            pos = self.input.search(inp, f"{pos}+{len(inp)}c", END)
        print()
    
    def change_tab(self, name, loaded_text):
        pass
        
    