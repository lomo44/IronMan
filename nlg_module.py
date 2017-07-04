
from subprocess import Popen, PIPE
from signal import SIGTERM
import os
import time
import requests
import json
class nlg_module(object):
    def __init__(self):
        self.nlg_server = None
        self.server_started = False
        self.host_name = ""
        self.host_port = -1
        self.output = open(os.devnull,"w")
        self.error = open(os.devnull,"w")
    def __del__(self):
        self.output.close()
        self.error.close()

    def start_server(self, hostname: str, port: int, output=None,error=None):
        if output == None:
            output = self.output

        if error == None:
            error = self.error

        self.host_name = hostname
        self.host_port = port
        print("Starting nlgserv on %s:%s" % (self.host_name, port))
        self.nlg_server = Popen(["java", "-jar",
                                 os.path.join(os.path.dirname(__file__),"nlgserv/nlgserv", "jython.jar"),
                                 os.path.join(os.path.dirname(__file__),"nlgserv/nlgserv", "_server.py"),
                                 self.host_name,
                                 str(self.host_port)],
                                stdin=PIPE,
                                stdout=output,
                                stderr=error)
        print("Waiting for server...")
        time.sleep(10)
        self.server_started = True
        pass

    def stop_server(self):
        self.nlg_server.kill()
        self.nlg_server.wait()
        self.server_started = False
        pass

    def send_data(self,dict):
        if self.server_started:
            req = requests.post("http://{0}:{1}/generateSentence".format(self.host_name,self.host_port),
                                  data=json.dumps({"sentence":dict}),
                                  headers={"Content-Type": "application/json"})
            return req.text
        else:
            return None

if __name__ == "__main__":
    a = nlg_module()
    a.start_server('localhost',8080)
    sentence = {}
    sentence["subject"] = "John"
    sentence["verb"] = "kick"
    sentence["object"] = "Dave"
    sentence["features"] = {"tense": "present"}
    q = a.send_data(sentence)
    print(q)
    a.stop_server()