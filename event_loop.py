from event_loop_status import eEvent_Loop_Status
from pipelines.basic_pipeline import basic_pipeline
from converse_context import converse_context

class event_loop(object):
    def __init__(self, pipeline:basic_pipeline):
        self.pipeline = pipeline

    def start(self):
        self.pipeline.attach_converse_context(converse_context())
        while True:
            user_input = self.pipeline.handle_input()
            self.pipeline.converse_context.history_input.append(user_input)
            self.pipeline.process(user_input);
            flag = self.pipeline.handle_output()
            if flag == eEvent_Loop_Status.eEvent_Loop_Exit:
                break

