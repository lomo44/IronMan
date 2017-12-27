from enum import Enum

class ePacket_flag(Enum):
    ePacketType_Unknown = 0,
    ePacketType_FB = 1
    ePacketType_Control = 3,
    ePacketType_NLU = 4,
    ePacketType_NLG = 5

class Base_packet(object):
    def __init__(self):
        self.type = ePacket_flag.ePacketType_Unknown

