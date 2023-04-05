import os
from tkinter.filedialog import asksaveasfilename, YES
from tkinter.messagebox import askquestion

userdir = os.path.expanduser("~")
pythonfilesdir = userdir + "\\python files\\"
master = None


def create(name: str, text: str, ext: str = ".py"):
    global master
    global pythonfilesdir
    if not os.path.exists(pythonfilesdir):
        os.makedirs(pythonfilesdir)
    if not name.strip() == "":
        if os.path.exists(pythonfilesdir + name + ext) and master.newfile.get() == "new":
            if askquestion("file already exists", "file already exists, do you want to replace?") == YES:
                file = open(pythonfilesdir + name + ext, 'w')
                file.write(text)
                file.close()
                master.file.set(name)
                master.state.set("saved")
                master.newfile.set("old")
        else:
            file = open(pythonfilesdir + name + ext, 'w')
            file.write(text)
            file.close()
            master.file.set(name)
            master.state.set("saved")
            master.newfile.set("old")
    else:
        name = asksaveasfilename(initialdir=pythonfilesdir)
        create(name.split("/")[-1], text)


def openfile(name: str):
    if len(name.split("/")) == 1 and len(name.split(".")) == 1:
        name = f'{pythonfilesdir}{name}.py'
    elif len(name.split("/")) == 1:
        name = f'{pythonfilesdir}{name}'
    elif len(name.split(".")) == 1:
        name = f'{pythonfilesdir}{name}'
    if os.path.exists(name):
        file = open(name, "r")
        fileinput = file.read()
        file.close()
        return [fileinput, True]
    else:
        return ["", False]
