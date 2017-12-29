from typing import List
from IronMan_MK1.modules.base.base_module import Base_module
from IronMan_MK1.modules.base.converse_context import Converse_context
from IronMan_MK1.modules.base.personality_context import Personality_context


class IM_NLG_Module(Base_module):
    def process(self, _input : List[Converse_context]):
        """
        Main function for processing list for converse context
        """
        pass
    def process_context(self, _input : Converse_context):
        """
        process individual context
        """
        pass
    def get_personality_reponse_templates(self, pContext : Personality_context):
        """
        based on personality context get its response templates
        """
        pass
    def initialize_template_library(self):
        """
        initialize template library
        """
        pass