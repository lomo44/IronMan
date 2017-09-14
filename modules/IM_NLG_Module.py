from modules.Base_module import Base_module, Module_packet, eBase_module_packet_flag

class IM_NLG_Module(Base_module):
    def process(self, _input : Module_packet):
        if _input.flag == eBase_module_packet_flag.eBase_module_packet_flag_TESTECHO:
            return _input