from input_modules.Base_input_module import Base_input_module, Module_packet


class scriptbook_input_module(Base_input_module):
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
                return Module_packet(output)
        return None
