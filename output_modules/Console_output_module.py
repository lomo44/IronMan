from output_modules.Base_output_module import Base_output_module,Module_packet


class console_output_module(Base_output_module):
    def __init__(self):
        pass
    def handle_output(self, input:Module_packet):
        print(Module_packet.payload)