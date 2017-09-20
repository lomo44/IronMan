from collections import deque

from modules.converse_context import converse_context

from input_modules.Base_input_module import Base_input_module
from modules.Module_packet import Module_packet, eModule_packet_flag
from modules.event_loop_status import eEvent_Loop_Status
from output_modules.Base_output_module import Base_output_module


class basic_pipeline(object):
    def __init__(self, input_module: Base_input_module, output_module: Base_output_module):
        self.input_module = input_module
        self.output_module = output_module
        self.converse_context = None
        self.on_create()
        self.modules = []
        self.output_deque = deque()
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

    def output(self, _output:Module_packet):
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

    def process(self, user_input:Module_packet):
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
            if user_input.flag == eModule_packet_flag.eBase_module_packet_flag_EXIT:
                return eEvent_Loop_Status.eEvent_Loop_Exit
            else:
                self.output_module.handle_output(user_input)
        return eEvent_Loop_Status.eEvent_Loop_Continue

    def add_logic_cores(self, core):
        """
        Add logic cores to the processor to further enlarge the command set
        :param core: new logic core
        """
        self.modules.append(core)
