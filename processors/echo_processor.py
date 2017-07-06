from processors.basic_processor import basic_processor
from event_loop_flags import event_loop_flags

class echo_processor(basic_processor):
    def get_input(self):
        return self.input_module.get_input()

    def get_output(self, user_input) -> event_loop_flags:
        if user_input == "quit":
            return event_loop_flags.event_loop_exit
        else:
            self.output_module.get_output(user_input)
            return event_loop_flags.event_loop_continue