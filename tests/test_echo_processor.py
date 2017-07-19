import unittest
from input_modules.scriptbook_input_module import scriptbook_input_module
from output_modules.scriptbook_output_module import scriptbook_output_module
from event_loop_module import event_loop_module
from processors.echo_processor import echo_processor


class test_echo_processor(unittest.TestCase):
    def test_basic_echo(self):
        input_module = scriptbook_input_module()
        input_module.set_script(["haha", "hehe", "quit"])
        output_module = scriptbook_output_module()
        c_m = event_loop_module(echo_processor(input_module, output_module))
        c_m.start()
        self.assertListEqual(output_module.retrieved_output, ["haha", "hehe"])
