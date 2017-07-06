from event_loop_flags import event_loop_flags
from converse_context import converse_context
from input_modules.base_input_module import base_input_module
from output_modules.base_output_module import base_output_module


class basic_processor(object):
    def __init__(self, input_module:base_input_module, output_module:base_output_module):
        self.input_module = input_module
        self.output_module = output_module
        self.converse_context = None
        pass

    def attach_converse_context(self, context: converse_context):
        self.converse_context = context

    def get_input(self):
        return NotImplemented

    def process(self, input):
        return NotImplemented

    def get_output(self, input) -> event_loop_flags:
        return NotImplemented
