from modules.Base_module import Base_module
from modules.Module_packet import eModule_packet_flag, Module_packet

class IM_Process_Module(Base_module):
    def process(self, _input : Module_packet):
        if _input.flag == eModule_packet_flag.eModule_packet_flag_test:
            _input.payload["output_payload"].append("IM_Process_Module")
        return _input