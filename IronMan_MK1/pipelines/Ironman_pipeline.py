from enum import Enum

from input_modules.Base_input_module import Base_input_module
from modules.IM_Control_Module import IM_Control_Module
from modules.IM_NLG_Module import IM_NLG_Module
from modules.IM_NLU_Module import IM_NLU_Module
from modules.IM_Process_Module import IM_Process_Module
from modules.Module_packet import Module_packet, eModule_packet_flag
from output_modules.Base_output_module import Base_output_module
from pipelines.Basic_pipeline import basic_pipeline

regex_Get = r"[g|G][e|E][t|T] (.*)"


class eIM_Data_Loading_Type(Enum):
    eIM_Data_Loading_Default = 0
    eIM_Data_Loading_Local = 1
    eIM_Data_Loading_Online = 2




class ironman_pipeline(basic_pipeline):
    def __init__(self, input_module: Base_input_module, output_module: Base_output_module):
        basic_pipeline.__init__(self, input_module, output_module)
        self.nlg_module = IM_NLG_Module()
        self.nlu_module = IM_NLU_Module()
        self.control_module = IM_Control_Module()
        self.process_module = IM_Process_Module()


    def load_data(self, data_loading_type: eIM_Data_Loading_Type):
        pass

    def process(self, input:Module_packet):
        newpayload = {
            "input_payload":input.payload,
            "output_payload": []
        }
        input.payload = newpayload
        control_output = self.control_module.process(input)
        if control_output.flag == eModule_packet_flag.eBase_module_packet_flag_EXIT:
            self.output(control_output)
        else:
            nlu_output = self.nlu_module.process(control_output)
            process_output = self.process_module.process(nlu_output)
            nlg_output = self.nlg_module.process(process_output)

            for item in nlg_output.payload["output_payload"]:
                self.output(Module_packet(item))
            return NotImplemented
