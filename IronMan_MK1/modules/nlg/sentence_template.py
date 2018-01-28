from IronMan_MK1.modules.base.nlg_recipe import NLG_Recipe
from typing import List
import re
import copy
from math import sqrt
from math import pow

def product(pools):
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

class Sentence_template(object):
    def __init__(self, pattern : str):
        self.pattern = set()
        self.pattern = pattern.split()

    def generate(self, nlg, recipe : NLG_Recipe):
        """
        Based on a recipe, generate a list of result tuples.
        result tuple format should be
        ([realization], [mean square root (msr) of the difference vector])
        """
        results = []
        if (not self.pattern):
            return
        positions = []
        wordchoices = []
        sentence = []
        for i, word in enumerate(self.pattern):
            match = re.match("\[(.+)\]",word)
            if match:
                if word=="[subject]":
                    sentence.append(recipe.generate_subjects())
                elif word=="[object]":
                    sentence.append(recipe.generate_objects())
                elif word=="[verb]":
                    sentence.append(recipe.generate_verb())
            else:
                match = re.match("{(.+)}",word)
                if match:
                    positions.append(i)
                    wordchoice = [word for word in nlg.nlg_data["lex"][match.group(1)]]
                    wordchoices.append(wordchoice)
                else:
                    assert False, "Bad template"
        products = product(wordchoices)
        for tup in products:
            attributes = dict.fromkeys(recipe.attribute.keys(), 1.0)
            s = copy.deepcopy(sentence)
            for i, word in enumerate(tup):
                s.insert(positions[i], word)
                match = re.match("{(.+)}", self.pattern[positions[i]])
                match = match.group(1)
                for attribute in attributes:
                    if attribute in nlg.nlg_data["lex"][match][word]:
                        attributes[attribute] = attributes[attribute] * nlg.nlg_data["lex"][match][word][attribute]
            s = ' '.join(s)
            msr = 0.
            for attribute in attributes:
                msr += pow(recipe.attribute[attribute] - attributes[attribute], 2.)
            msr = sqrt(msr)
            results.append((msr,s))
        return results


    def is_compatible(self, recipe : NLG_Recipe) -> bool:
        """ 
        Check if the given recipe is compatible with current template
        """
        if not self.is_in_pattern(recipe, "[subject]"):
            return False
        if not self.is_in_pattern(recipe, "[object]"):
            return False
        if not self.is_in_pattern(recipe, "[verb]"):
            return False
        return True

    def is_in_pattern(self, recipe : NLG_Recipe, elem) -> bool:
        if (recipe.requirement[elem] and elem not in self.pattern):
            return False
        elif (not recipe.requirement[elem]  and elem in self.pattern):
            return False
        return True
