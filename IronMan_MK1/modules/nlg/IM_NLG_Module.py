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
import random

re_requirement = re.compile("\[.*\]")

class IM_NLG_Module(Base_module):
    def __init__(self):
        self.nlg_data = None
        self.load_nlg_data("IronMan_MK1/modules/nlg/iron_man_data.json")
        #self.templates : Dict[str,Sentence_template] = {} # type : Dict[str, Sentence_template]
        self.templates = {}
        self.initialize_template()

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

    def select_result(self, recipe : NLG_Recipe, results):
        """
        Given a list of results, select the proper one
        """
        results = sorted(results)
        accepted = -1
        size = len(results)
        for i in range(size):
            if results[i][0] == 0.:
                accepted = i
            else:
                break
        if accepted== -1:
            return self.nlg_data["default"]
        else:
            return results[random.randrange(accepted)][1]



    def realization(self, recipe : NLG_Recipe) -> str:
        """
        Generate the realization based on the sentence"
        """
        results = []
        for template_name in self.templates:
            if (self.templates[template_name].is_compatible(recipe)):
                results.extend(self.templates[template_name].generate(self, recipe))
        return self.select_result(recipe, results)