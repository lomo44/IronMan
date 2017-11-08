from modules.Module_packet import Module_packet

class Base_input_module(object):
    def __init__(self):
        pass

    def handle_input(self) -> Module_packet:
        return NotImplemented
