import nlgserv.nlgserv
import time

class nlg_module(object):
    def __init__(self):
        self.nlg_server = None
        self.server_started = False
        self.host_name = ""
        self.host_port = -1

    def start_server(self, hostname: str, port: int):
        self.host_name = hostname
        self.host_port = port
        self.nlg_server = nlgserv.nlgserv.start_server(hostname,port)
        print("Waiting for server...")
        time.sleep(20)
        pass

    def stop_server(self):
        nlgserv.nlgserv.stop_server(self.nlg_server)
        pass

