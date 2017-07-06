from output_modules.base_output_module import base_output_module


class console_output_module(base_output_module):
    def __init__(self):
        pass
    def get_output(self, input):
        print(input)