from event_loop_flags import event_loop_flags
from converse_context import converse_context
class basic_processor(object):
    def __init__(self):
        self.converse_context = None
        pass

    def attach_converse_context(self, context:converse_context):
        self.converse_context = context

    def get_input(self):
        return NotImplemented

    def get_output(self,input) -> event_loop_flags:
        return NotImplemented