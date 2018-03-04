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
import copy
from functools import lru_cache

content_prog = re.compile("\[(.*)\]")
descriptor_prog = re.compile("{(.*)}")
verb_prog = re.compile("\((.*)\)")
subtemplate_prog = re.compile("<(.*)>")

def Product(pools):
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

class IM_NLG_Module(Base_module):
    def __init__(self, json_file="IronMan_MK1/modules/nlg/iron_man_data.json"):
        self.nlg_data = None
        self.LoadNLGData(json_file)
        # Make sure there are default responses (at least one)
        defaults = self.nlg_data["default"]
        num_defaults = len(defaults)
        assert num_defaults > 0, "Default responses are missing in the json file!"
        #self.templates : Dict[str,Sentence_template] = {} # type : Dict[str, Sentence_template]
        #self.templates = {}
        #self.initialize_template()

    def LoadNLGData(self, path : str):
        """
        Load the nlg_data from file
        """
        with open(path,'r') as template_file:
            loaded_data = json.load(template_file)
            if "ID" in loaded_data:
                self.nlg_data = loaded_data

    def SelectResult(self, recipe : NLG_Recipe, results):
        """
        Given a list of results, select the proper one
        """
        size = len(results)
        if (size > 0):
            pick = random.randint(0, size-1)
            return results[pick]
        else:
            defaults = list(self.nlg_data["default"])
            num_defaults = len(defaults)
            pick = random.randint(0, num_defaults-1)
            return defaults[pick]


    @lru_cache(maxsize=128)
    def TemplateTokenizer(self, template):
        tokenized_template = template.split()
        return tokenized_template

    # TODO
    def ChangeTense(self, verb, tense="VB"):
        return verb
    
    def SubtemplateRealization(self, content_index, expected_end_index, recipe, missing_attributes, subtemplate_type):
        """
        Generate sub-sentences that will be plugged back into the original template that contains this
        subtemplate.
        """
        subsentences = []
        attribute_keys = set(missing_attributes.keys())
        for subtemplate in self.nlg_data["sub-templates"][subtemplate_type]:
            tmp_content_index = content_index
            sentence = ""
            valid_template = True
            if set(self.nlg_data["sub-templates"][subtemplate_type][subtemplate]) != attribute_keys:
                continue
            for attribute in self.nlg_data["sub-templates"][subtemplate_type][subtemplate]:
                if self.nlg_data["sub-templates"][subtemplate_type][subtemplate][attribute] != missing_attributes[attribute]:
                    valid_template = False
                    break
            if not valid_template:
                continue
            tokenized_template = self.TemplateTokenizer(subtemplate)
            for token in tokenized_template:
                # token = [content]
                match = content_prog.match(token)
                if match:
                    if (tmp_content_index >= len(recipe.contents)):
                        vaild_template = False
                        break
                    else:
                        sentence += " " + recipe.contents[tmp_content_index]
                        tmp_content_index += 1
                        continue
                # token ~= "(verb)"
                match = verb_prog.match(token)
                if match:
                    verb = match.group(1)
                    verb = self.ChangeTense(verb, recipe.tense)
                    sentence += " " + verb
                    continue
                sentence += " " + token
            if (valid_template):
                if(tmp_content_index == expected_end_index):
                    subsentences.append(sentence)
        if (len(subsentences) > 0):
            missing_attributes.clear()

        return subsentences





    def Realization(self, recipe : NLG_Recipe) -> str:
        """
        Generate sentences based on the recipe"
        Assume each template only has at most one sub-template, which does not contain any sub-template itself
        """
        results = []
        if recipe.intent not in self.nlg_data["templates"]:
            print("Invalid Intent. Intent must be one of: " + " ".join(self.nlg_data["templates"]))
            return results

        for template in self.nlg_data["templates"][recipe.intent]:
            vaild_template = True
            sentences = ["", ""]
            subsentences = []
            final_sentences = []
            sentence_index = 0
            missing_attributes = copy.deepcopy(recipe.attributes)
            keys = recipe.attributes.keys()
            descriptors_template = set()
            for attribute in self.nlg_data["templates"][recipe.intent][template]:
                if attribute not in keys or self.nlg_data["templates"][recipe.intent][template][attribute]!= recipe.attributes[attribute]:
                    #template has extra attributes that recipe does not have, or template's attribute's value does mot equal to recipe's attribute's value
                    vaild_template = False
                    break
                else:
                    del missing_attributes[attribute]
            if not vaild_template:
                continue
            tokenized_template = self.TemplateTokenizer(template)
            content_index = 0
            expected_subtemplate_end_content_index = 0
            has_subtemplate = False
            for token in reversed(tokenized_template):
                if subtemplate_prog.match(token):
                    break
                if content_prog.match(token):
                    expected_subtemplate_end_content_index += 1
            expected_subtemplate_end_content_index = len(recipe.contents) - expected_subtemplate_end_content_index
            if expected_subtemplate_end_content_index < 0:
                continue

            for token in tokenized_template:
                # token = [content]
                match = content_prog.match(token)
                if match:
                    if (content_index >= len(recipe.contents)):
                        vaild_template = False
                        break
                    else:
                        sentences[sentence_index] += " " + recipe.contents[content_index]
                        content_index += 1
                        continue
                # token ~ "{descriptor}"
                match = descriptor_prog.match(token)
                if match:
                    descriptor = match.group(1)
                    if descriptor not in recipe.descriptors.keys():
                        vaild_template = False
                        break
                    else:
                        sentences[sentence_index] += " " + recipe.descriptors[descriptor]
                        descriptors_template.add(descriptor)
                    continue
                # token ~= "(verb)"
                match = verb_prog.match(token)
                if match:
                    verb = match.group(1)
                    verb = self.ChangeTense(verb, recipe.tense)
                    sentences[sentence_index] += " " + verb
                    continue
                # token ~= "<subtemplate>"
                match = subtemplate_prog.match(token)
                if match:
                    subtemplate = match.group(1)
                    subsentences = self.SubtemplateRealization(content_index, expected_subtemplate_end_content_index, recipe, missing_attributes, subtemplate)
                    content_index = expected_subtemplate_end_content_index
                    sentence_index = 1
                    continue
                sentences[sentence_index] += " " + token

            if vaild_template:
                 # Three more things to check
                 # 1. Have we matched all the attributes in the recipe?
                 if(len(missing_attributes)==0):
                    # 2. Have we consumed all the contents in the recipe?
                    if (content_index == len(recipe.contents)):
                        if (len(subsentences) > 0):
                            for subsentence in subsentences:
                                final_sentences.append(sentences[0] + " " + subsentence + " " + sentences[1])
                        else:
                            final_sentences.append(sentences[0])
                    # 3. Append any unused descriptors in the recipe
                        unused_descriptors = set(recipe.descriptors) - descriptors_template
                        size = len(final_sentences)
                        for idx in range(size):
                            for unused_descriptor in unused_descriptors:
                                final_sentences[idx] += " " + unused_descriptors
                    results.extend(final_sentences)
        return results





        #for template_name in self.templates:
            #if (self.templates[template_name].is_compatible(recipe)):
                #results.extend(self.templates[template_name].generate(self, recipe))
        #return self.SelectResult(recipe, results)