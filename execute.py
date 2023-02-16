import subprocess as sp
import threading as th
import files

master = None



def Execute(name):
    global master
    master.del_cons()
    p = sp.Popen(["C:/Users/Gebruiker/AppData/Local/Programs/Python/Python39/python.exe", files.userdir + "/python files/" + name + ".py"], stdout=sp.PIPE)
    while p.poll() is None:
        out = p.stdout.read()
        master.ins_cons(out)
