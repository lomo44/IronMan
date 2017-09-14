import unittest
from input_modules.Scriptbook_input_module import scriptbook_input_module
from output_modules.Scriptbook_output_module import scriptbook_output_module
from event_loop import event_loop
from pipelines.Echo_pipeline import echo_pipeline


class test_echo_processor(unittest.TestCase):
    def test_basic_echo(self):
        input_module = scriptbook_input_module()
        input_module.set_script(["haha", "hehe", "quit"])
        output_module = scriptbook_output_module()
        c_m = event_loop(echo_pipeline(input_module, output_module))
        c_m.start()
        self.assertListEqual(output_module.retrieved_output, ["haha", "hehe"])
