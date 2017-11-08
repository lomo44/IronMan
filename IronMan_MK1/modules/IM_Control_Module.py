from modules.Base_module import Base_module
from modules.Module_packet import eModule_packet_flag, Module_packet

class IM_Control_Module(Base_module):
    def process(self, _input : Module_packet):
        if _input.payload["input_payload"] == "test/echo":
            _input.flag = eModule_packet_flag.eModule_packet_flag_test
        if _input.payload["input_payload"] == "quit":
            _input.flag = eModule_packet_flag.eBase_module_packet_flag_EXIT
        if _input.flag == eModule_packet_flag.eModule_packet_flag_test:
            _input.payload["output_payload"].append("IM_Control_Module")
        return _input
