from enum import Enum

class eModule_packet_flag(Enum):
    eBase_module_packet_flag_OK = 0,
    eBase_module_packet_flag_SKIP = 1,
    eBase_module_packet_flag_EXIT = 2,
    eBase_module_packet_flag_TESTECHO = 3

class Module_packet(object):
    def __init__(self):
        self.payload = None
        self.flag = eModule_packet_flag.eBase_module_packet_flag_OK
    def __init__(self, payload):
        self.payload = payload
        self.flag = eModule_packet_flag.eBase_module_packet_flag_OK
