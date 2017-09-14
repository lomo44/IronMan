from pipelines.basic_pipeline import basic_pipeline
from event_loop_status import eEvent_Loop_Status

class echo_pipeline(basic_pipeline):
    def process(self, user_input):
        if user_input == 'quit':
            self.output(self.QUIT_COMMAND)
        else:
            return self.output(user_input)
