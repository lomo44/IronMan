from event_loop_status import eEvent_Loop_Status
from converse_context import converse_context
from input_modules.base_input_module import base_input_module
from output_modules.base_output_module import base_output_module
from collections import deque


class basic_processor(object):
    def __init__(self, input_module: base_input_module, output_module: base_output_module):
        self.input_module = input_module
        self.output_module = output_module
        self.converse_context = None
        self.on_create()
        self.logic_cores = []
        self.output_deque = deque()
        self.QUIT_COMMAND = "quit"
        pass

    def on_create(self):
        """
        This function is called when processor is created. You can do some basic initialization here
        """
        pass

    def attach_converse_context(self, context: converse_context):
        """
        Call this function to attach a converse context to record user input
        :param context: new converse context
        """
        self.converse_context = context

    def output(self, _output: str):
        """
        Use this function to pipe out output, 
        :param _output: string to output
        """
        self.output_deque.append(_output)

    def handle_input(self) -> str:
        """
        Get input from input module. It is developer's job to propagate the user control message
        :return: Input string from input module, could be keyboard input or script book input
        """
        return self.input_module.handle_input()

    def process(self, user_input: str):
        """
        Process the user input and generate corresponding output, should be overloaded for each processer
        :param user_input: input string from the input module
        """
        return NotImplemented

    def handle_output(self) -> eEvent_Loop_Status:
        """
        Handle program's output, and propagate the output to output module. This function will drain everything in the
        output deque. If there is a QUIT_COMMAND inside the deque, the output handling will stop and return an exit flag
        :return: eEvent_Loop_Continue if no QUIT_COMMAND in the output, or eEvent_Loop_Exit
        """
        while len(self.output_deque) is not 0:
            user_input = self.output_deque.pop()
            if user_input == self.QUIT_COMMAND:
                return eEvent_Loop_Status.eEvent_Loop_Exit
            else:
                self.output_module.handle_output(user_input)
        return eEvent_Loop_Status.eEvent_Loop_Continue

    def add_logic_cores(self, core):
        """
        Add logic cores to the processor to further enlarge the command set
        :param core: new logic core
        """
        self.logic_cores.append(core)
