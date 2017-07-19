from input_modules.base_input_module import base_input_module


class scriptbook_input_module(base_input_module):
    def __init__(self):
        self.counter = 0
        self.script = None

    def set_script(self, script: list):
        self.script = script

    def handle_input(self):
        if self.script is not None:
            if self.counter < len(self.script):
                output = self.script[self.counter]
                self.counter += 1
                return output
        return None
