from processors.basic_processor import basic_processor
from event_loop_status import eEvent_Loop_Status

class echo_processor(basic_processor):
    def process(self, user_input):
        if user_input == 'quit':
            self.output(self.QUIT_COMMAND)
        else:
            return self.output(user_input)
