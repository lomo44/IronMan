from IronMan_MK1.modules.base.nlg_recipe import NLG_Recipe
from typing import List

class Sentence_template(object):
    def __init__(self, pattern : str):
        self.pattern = pattern
        self.parse_pattern(pattern)
        
    def generate(self,recipe : NLG_Recipe):
        """
        Based on a recipe, generate a list of result turples.
        result turple format should be
        ([relization], [distance to recipe vector])
        """
        pass
    def is_compatible(self, recipe : NLG_Recipe) -> bool:
        """ 
        Check if the given recipe is compatible with current template
        """
        pass
    def parse_pattern(self, pattern : str):
        """
        parse the current template
        """
        pass