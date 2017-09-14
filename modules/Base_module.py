
from modules.Module_packet import Module_packet


class Base_module(object):
    def __init__(self, processor):
        self.processor = processor

    def process(self, _input : Module_packet) -> Module_packet:
        return NotImplemented


