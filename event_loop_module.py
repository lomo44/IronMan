from event_loop_status import eEvent_Loop_Status
from processors.basic_processor import basic_processor
from converse_context import converse_context

class event_loop_module(object):
    def __init__(self, processor:basic_processor):
        self.processor = processor

    def start(self):
        self.processor.attach_converse_context(converse_context())
        while True:
            user_input = self.processor.handle_input()
            self.processor.converse_context.history_input.append(user_input)
            self.processor.process(user_input);
            flag = self.processor.handle_output()
            if flag == eEvent_Loop_Status.eEvent_Loop_Exit:
                break

