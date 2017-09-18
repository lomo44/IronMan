import unittest
from input_modules.Scriptbook_input_module import scriptbook_input_module
from output_modules.Scriptbook_output_module import scriptbook_output_module
from event_loop import event_loop
from pipelines.Ironman_pipeline import ironman_pipeline

class test_IM_pipeline(unittest.TestCase):
    def setUp(self):
        self.input_module = scriptbook_input_module()
        self.output_module = scriptbook_output_module()
        self.loop = event_loop(ironman_pipeline(self.input_module,self.output_module))

    def test_IM_pipeline_echo(self):
        self.input_module.set_script(["test/echo","quit"])
        self.loop.start()
        self.assertListEqual(self.output_module.retrieved_output, ["IM_NLG_Module", "IM_Process_Module","IM_NLU_Module", "IM_Control_Module"])

        pass

