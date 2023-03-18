import subprocess as sp
import threading as th
import time
import files
import code_editor
import sys


master = None
process = None


def refresh(last_out, last_err):
    global master
    with open("stdout.txt", "r") as stdout:
        out = stdout.read()
        last_out_end = out.rindex(last_out) + len(last_out)
        ins_out = out[last_out_end:]
    with open("stderr.txt", "r") as stderr:
        err = stderr.read()
        last_err_end = err.rindex(last_err) + len(last_err)
        ins_err = err[last_err_end:]
    master.ins_cons(ins_out)
    master.ins_cons(ins_err, err=True)
    return out, err


def Execute(name):
    global process
    print(time.time())
    outfile = open("stdout.txt", "w")
    errfile = open("stderr.txt", "w")
    process = sp.Popen(["C:/Users/Gebruiker/AppData/Local/Programs/Python/Python39/python.exe", files.userdir + "/python files/" + name + ".py"],
                       stdout=outfile,
                       stderr=errfile,
                       stdin=sys.stdin)

    stdout = ""
    stderr = ""
    while True:
        if process.poll() is not None:
            break
        else:
            stdout, stderr = refresh(stdout, stderr)

    print(time.time())


def kill():
    global process
    if process is not None:
        process.terminate()
        process.kill()
