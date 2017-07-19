from processors.basic_processor import basic_processor
from event_loop_status import eEvent_Loop_Status

class echo_processor(basic_processor):
    def handle_input(self):
        return self.input_module.handle_input()

    def process(self, user_input):
        return user_input

    def handle_output(self, user_input) -> eEvent_Loop_Status:
        if user_input == "quit":
            return eEvent_Loop_Status.eEvent_Loop_Exit
        else:
            self.output_module.handle_output(user_input)
            return eEvent_Loop_Status.eEvent_Loop_Continue