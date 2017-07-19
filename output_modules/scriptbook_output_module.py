from output_modules.base_output_module import base_output_module

class scriptbook_output_module(base_output_module):
    def __init__(self):
        self.retrieved_output = []
    def handle_output(self, user_input):
        self.retrieved_output.append(user_input)