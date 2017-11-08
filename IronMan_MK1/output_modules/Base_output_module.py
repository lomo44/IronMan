from modules.Base_module import Module_packet
class Base_output_module(object):
    def __init__(self):
        pass
    def handle_output(self, input:Module_packet):
        return NotImplemented