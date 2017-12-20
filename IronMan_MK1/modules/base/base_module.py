
from IronMan_MK1.modules.base.base_packet import Base_packet


class Base_module(object):
    def __init__(self):
        pass

    def process(self, _input : Base_packet) -> Base_packet:
        return NotImplemented


