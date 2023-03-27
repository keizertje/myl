import subprocess as sp
import threading as th
import files
import sys


master = None
process = None


def refresh(last_out, last_err):
    global master
    with open("stdout.txt", "r") as stdout:
        out = stdout.read()
        last_out_end = out.index(last_out) + len(last_out)
        ins_out = out[last_out_end:]
    with open("stderr.txt", "r") as stderr:
        err = stderr.read()
        last_err_end = err.index(last_err) + len(last_err)
        ins_err = err[last_err_end:]
    master.ins_cons(ins_out)
    master.ins_cons(ins_err, err=True)
    return out, err


def stdin(chars):
    global process
    if process is not None:
        process.communicate(input=chars)
    else:
        pass


def Execute(name):
    global master
    global process
    process = None
    stdout = ""
    stderr = ""
    outfile = open("stdout.txt", "w")
    errfile = open("stderr.txt", "w")
    while True:
        if process is None:
            process = sp.Popen(["C:/Users/Gebruiker/AppData/Local/Programs/Python/Python39/python.exe", files.userdir + "/python files/" + name + ".py"],
                               stdout=outfile,
                               stderr=errfile,
                               stdin=sp.PIPE,
                               text=True)
        if process is not None:
            if process.poll() is not None:
                break
            else:
                stdout, stderr = refresh(stdout, stderr)
    refresh(stdout, stderr)
    master.ins_cons("Process finished with exit code " + str(process.poll()) + "\n")
    process = None
