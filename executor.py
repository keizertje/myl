import os
import time
from subprocess import *
import threading


class Executor:
    def __init__(self, write_fn):
        self.process: Popen | None = None
        self.input_thread = None
        self.write_fn = write_fn

    def read_stdout(self):
        os.set_blocking(self.process.stdout.fileno(), False)
        while self.process.poll() is None:
            char = self.process.stdout.read()
            if char:
                self.write_fn(char.decode())

        while not self.process.stdout.closed:
            char = self.process.stdout.read()
            if char:
                self.write_fn(char.decode())
            else:
                self.process.stdout.close()

    def read_stderr(self):
        os.set_blocking(self.process.stderr.fileno(), False)
        while self.process.poll() is None:
            char = self.process.stderr.read()
            if char:
                self.write_fn(char.decode(), {"foreground": "red"})

        while not self.process.stderr.closed:
            char = self.process.stderr.read()
            if char:
                self.write_fn(char.decode(), {"foreground": "red"})
            else:
                self.process.stderr.close()

    def write_exitcode(self, x1, x2):
        while x1.is_alive() or x2.is_alive():
            time.sleep(0.05)
        self.write_fn(f"Process finished with exit code {self.process.wait()}\n", {"foreground": "blue"})

    def write_stdin(self, __s):
        self.process.stdin.write(__s.encode())
        self.process.stdin.flush()

    @property
    def is_running(self):
        print(f"self.process = {self.process}")
        return self.process.poll() is None

    def start(self, cmd):
        self.process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        x1 = threading.Thread(target=self.read_stdout, daemon=True)
        x2 = threading.Thread(target=self.read_stderr, daemon=True)
        x3 = threading.Thread(target=self.write_exitcode, args=(x1, x2), daemon=True)
        x1.start()
        x2.start()
        x3.start()