import subprocess
import threading


class Execute:
    def __init__(self, console):
        self.console = console
        self.process = None

    def read_output(self):
        while True:
            char = self.process.stdout.read(1)
            if char:
                self.console.write(char)
            else:
                break
        self.process.wait()
        self.console.write(f"\nProcess finished with exit code {self.process.poll()}\n")
        self.process.stdout.close()

    def send_input(self, __s):
        if self.process.poll() is None:
            self.process.stdin.write(__s)
            self.process.stdin.flush()

    @property
    def is_running(self):
        return self.process.poll() is None

    def start(self, command):
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        threading.Thread(target=self.read_output, daemon=True).start()
