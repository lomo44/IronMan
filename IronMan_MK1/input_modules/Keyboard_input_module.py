from input_modules.Base_input_module import Base_input_module
from modules.Module_packet import Module_packet


class keyboard_input_module(Base_input_module):
    def __init__(self):
        pass

    def handle_input(self):
        return Module_packet(input("Enter Input:"))
