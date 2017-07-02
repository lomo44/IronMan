
from subprocess import Popen, PIPE
from signal import SIGTERM
import os
import time

class nlg_module(object):
    def __init__(self):
        self.nlg_server = None
        self.server_started = False
        self.host_name = ""
        self.host_port = -1

    def start_server(self, hostname: str, port: int, output=None,error=None):
        if output == None:
            output = open(os.devnull, "w")

        if error == None:
            error = open(os.devnull, "w")

        self.host_name = hostname
        self.host_port = port
        print("Starting nlgserv on %s:%s" % (self.host_name, port))
        print(os.path.join(os.path.dirname(__file__),"nlgserv/nlgserv","jython.jar"))
        self.nlg_server = Popen(["java", "-jar",
                                 os.path.join(os.path.dirname(__file__),"nlgserv/nlgserv", "jython.jar"),
                                 os.path.join(os.path.dirname(__file__),"nlgserv/nlgserv", "_server.py"),
                                 self.host_name,
                                 str(self.host_port)],
                                stdin=PIPE,
                                stdout=output,
                                stderr=error)
        print("Waiting for server...")
        time.sleep(20)
        pass

    def stop_server(self):
        self.nlg_server.kill()
        self.nlg_server.wait()
        pass

if __name__ == "__main__":
    a = nlg_module()
    a.start_server('localhost',8080)
    a.stop_server()