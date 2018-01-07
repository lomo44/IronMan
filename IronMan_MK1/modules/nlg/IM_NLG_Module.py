from typing import List,Dict
from IronMan_MK1.modules.base.base_module import Base_module
from IronMan_MK1.modules.base.converse_context import Converse_context
from IronMan_MK1.modules.base.personality_context import Personality_context
from IronMan_MK1.modules.base.nlg_recipe import NLG_Recipe
from IronMan_MK1.modules.nlg.sentence_template import Sentence_template
import json
import os
import sys
import re

re_requirement = re.compile("\[.*\]")

class IM_NLG_Module(Base_module):
    def __init__(self):
        self.nlg_data = None
        self.load_nlg_data("IronMan_MK1/modules/nlg/iron_man_template.json")
        self.templates : Dict[str,Sentence_template] = {} # type : Dict[str, Sentence_template]

    def load_nlg_data(self,path : str):
        """
        Load the nlg_data from file
        """
        with open(path,'r') as template_file:
            loaded_data = json.load(template_file)
            if "ID" in loaded_data:
                self.nlg_data = loaded_data
                
    def initialize_template(self):
        """
        Based on loaded data, initialize templates
        """
        if "templates" in self.nlg_data:
            for item in self.nlg_data["templates"]:
                if "pattern" in self.nlg_data["templates"][item]:
                    # initialize templates using its pattern and name
                    self.templates[item] = Sentence_template(self.nlg_data["templates"][item]["pattern"])

    def select_result(self, results)
        """
        Given a list of results, select the proper one
        """
        pass

    def realization(self, recipe : NLG_Recipe) -> str:
        """
        Generate the realization based on the sentense"
        """
        results = []
        for template_name in self.templates:
            result += self.templates[template_name].generate(recipe)
        return select_result(results)[0]