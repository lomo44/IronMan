from output_modules.Base_output_module import Base_output_module
from modules.Module_packet import Module_packet

class scriptbook_output_module(Base_output_module):
    def __init__(self):
        self.retrieved_output = []
    def handle_output(self, user_input:Module_packet):
        self.retrieved_output.append(user_input.payload)