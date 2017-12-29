from typing import List
from IronMan_MK1.modules.base.base_module import Base_module
from IronMan_MK1.modules.base.converse_context import Converse_context
from IronMan_MK1.modules.base.personality_context import personality_context


class IM_NLG_Module(Base_module):
    def process(self, _input : List[Converse_context]):
        pass
    def process_context(self, _input : Converse_context):
        pass
    def load_personality_reponse_template()