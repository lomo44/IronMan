from IronMan_MK1.modules.base.nlg_recipe import NLG_Recipe
from typing import List
import re
import copy
from math import sqrt
from math import pow

content_prog = re.compile("\[(.*)\]")
descriptor_prog = re.compile("{(.*)}")
verb_prog = re.compile("\[verb\]")
subtemplate_prog = re.compile("<(.*)>")

class Sentence_Template(object):
    def __init__(self, pattern : str, attributes):
        self.pattern = pattern.split()
        self.attributes = {}
        self.contents = set()
        self.descriptors = set()
        self.hasSubtemplate = False
        for attribute in attributes:
            self.attributes[attribute] = attributes[attribute]
        for token in self.pattern:
            # token = [content]
            match = content_prog.match(token)
            if match:
                self.contents.add(match.group(1))
                continue

            match = subtemplate_prog.match(token)
            if match:
                self.hasSubtemplate = True

            match = descriptor_prog.match(token)
            if match:
                self.descriptors.add(match.group(1))