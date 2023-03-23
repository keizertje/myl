import os
from alert import alert
from tkinter.filedialog import asksaveasfilename

userdir = os.path.expanduser("~")
master = None


def create(name: str, text: str, ext: str = ".py"):
    global master
    global userdir
    if not os.path.exists(userdir + "/python files"):
        os.makedirs(userdir + "/python files")
    if not name.strip() == "":
        if os.path.exists(f'{userdir}/python files/{name}{ext}') and master.newfile.get() == "new":
            if alert(msg="file already exists, do you want to replace?", button_b_msg="No", button_a_msg="Yes") == "Yes":
                file = open(f'{userdir}/python files/{name}{ext}', 'w')
                file.write(text)
                file.close()
                master.file.set(name)
                master.state.set("saved")
                master.newfile.set("old")
        else:
            file = open(f'{userdir}/python files/{name}{ext}', 'w')
            file.write(text)
            file.close()
            master.file.set(name)
            master.state.set("saved")
            master.newfile.set("old")
    else:
        name = asksaveasfilename(initialdir=userdir + "/python files/")
        create(name.split("/")[-1], text)


def openfile(name: str):
    if len(name.split("/")) == 1 and len(name.split(".")) == 1:
        name = f'{userdir}/python files/{name}.py'
    elif len(name.split("/")) == 1:
        name = f'{userdir}/python files/{name}'
    elif len(name.split(".")) == 1:
        name = f'{userdir}/python files/{name}'
    if os.path.exists(name):
        file = open(name, "r")
        fileinput = file.read()
        file.close()
        return [fileinput, True]
    else:
        return ["", False]
