from input_modules.base_input_module import base_input_module


class keyboard_input_module(base_input_module):
    def __init__(self):
        pass

    def get_input(self):
        return input("Enter Input: ")
