from modules.Module_packet import Module_packet, eModule_packet_flag
from pipelines.Basic_pipeline import basic_pipeline


class echo_pipeline(basic_pipeline):
    def process(self, user_input:Module_packet):
        if user_input.payload == 'quit':
            user_input.flag = eModule_packet_flag.eBase_module_packet_flag_EXIT
        return self.output(user_input)
