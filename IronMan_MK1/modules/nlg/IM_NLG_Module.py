from typing import List
from IronMan_MK1.modules.base.base_module import Base_module
from IronMan_MK1.modules.base.converse_context import Converse_context
from IronMan_MK1.modules.base.personality_context import Personality_context
from IronMan_MK1.modules.base.nlg_recipe import NLG_Recipe
import json
import os
import sys
import re

re_requirement = re.compile("\[.*\]")

class IM_NLG_Module(Base_module):
    def __init__(self):
        self.template = None
        print(os.getcwd())
        self.load_templates("IronMan_MK1/modules/nlg/iron_man_template.json")

    def load_templates(self,path : str):
        with open(path,'r') as template_file:
            template = json.load(template_file)
            if "ID" in template:
                self.template = template
                
    def is_template_usable(self, recipe : NLG_Recipe, pattern : str) -> bool:
        pass

    def realization(self, recipe : NLG_Recipe) -> str:
        pass