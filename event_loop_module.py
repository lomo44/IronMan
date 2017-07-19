from event_loop_status import eEvent_Loop_Status
from processors.basic_processor import basic_processor
from processors.echo_processor import echo_processor
from converse_context import converse_context
from input_modules.keyboard_input_module import keyboard_input_module
from output_modules.console_output_module import console_output_module
from input_modules.scriptbook_input_module import scriptbook_input_module
from output_modules.scriptbook_output_module import scriptbook_output_module
class event_loop_module(object):
    def __init__(self, processor:basic_processor):
        self.processor = processor

    def start(self):
        self.processor.attach_converse_context(converse_context())
        while True:
            user_input = self.processor.handle_input()
            self.processor.converse_context.history_input.append(user_input)
            output = self.processor.process(user_input);
            flag = self.processor.handle_output(output)
            if flag == eEvent_Loop_Status.eEvent_Loop_Exit:
                break

if __name__ == "__main__":
    input_module = scriptbook_input_module()
    input_module.set_script(["haha","hehe","quit"])
    output_module = scriptbook_output_module()
    c_m = event_loop_module(echo_processor(input_module,output_module))
    c_m.start()
    print(output_module.retrieved_output)

