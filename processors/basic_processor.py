from event_loop_status import eEvent_Loop_Status
from converse_context import converse_context
from input_modules.base_input_module import base_input_module
from output_modules.base_output_module import base_output_module


class basic_processor(object):
    def __init__(self, input_module:base_input_module, output_module:base_output_module):
        self.input_module = input_module
        self.output_module = output_module
        self.converse_context = None
        self.on_create()
        self.logic_cores = []
        pass

    def on_create(self):
        pass

    def attach_converse_context(self, context: converse_context):
        self.converse_context = context

    def handle_input(self):
        return NotImplemented

    def process(self, input):
        return NotImplemented

    def handle_output(self, input) -> eEvent_Loop_Status:
        return NotImplemented

    def add_logic_cores(self, core):
        self.logic_cores.append(core)