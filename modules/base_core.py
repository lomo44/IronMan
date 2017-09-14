from pipelines import basic_pipeline
from event_loop_status import eCommand_Process_Status

class base_core(object):
    def __init__(self, processor: basic_pipeline):
        self.processor = processor

    def process(self, _input):
        return NotImplemented