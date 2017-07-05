from processors.basic_processor import basic_processor
from event_loop_flags import event_loop_flags

class echo_processor(basic_processor):
    def __init__(self):
        pass
    def get_input(self):
        return input("Enter Input:")
    def get_output(self,input) -> event_loop_flags:
        if input == "quit":
            return event_loop_flags.event_loop_exit
        else:
            print(input)
            return event_loop_flags.event_loop_continue