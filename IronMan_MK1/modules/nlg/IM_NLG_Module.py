from IronMan_MK1.modules.base.base_module import Base_module
from IronMan_MK1.modules.base.nlg_recipe import NLG_Recipe
from IronMan_MK1.modules.nlg.sentence_template import Sentence_Template
import json
import re
import random
import IronMan_MK1.modules.nlg.utility as utility
import spacy

content_prog = re.compile("\[(.*)\]")
descriptor_prog = re.compile("{(.*)}")
verb_prog = re.compile("\[verb\]")
subtemplate_prog = re.compile("<(.*)>")

modal_verb_list = ["can", "could", "may", "might", "will", "would", "shall", "should", "must"]

class IM_NLG_Module(Base_module):
    def __init__(self, json_file="IronMan_MK1/modules/nlg/iron_man_data.json"):
        self.nlg_data = None
        self.templates = {}
        self.subtemplates = {}
        self.defaults = {}
        self.LoadNLGData(json_file)
        self.parseNLGData()
        #TODO should be loaded in the main pipeline?
        self.nlp = spacy.load('en')
        del self.nlg_data
        # Make sure there are default responses (at least one)
        #defaults = self.nlg_data["default"]
        #num_defaults = len(defaults)
        #assert num_defaults > 0, "Default responses are missing in the json file!"


    def LoadNLGData(self, path : str):
        """
        Load the nlg_data from file
        """
        with open(path,'r') as template_file:
            loaded_data = json.load(template_file)
            if "ID" in loaded_data:
                self.nlg_data = loaded_data

    def SelectResult(self, results):
        """
        Given a list of results, select the proper one
        """
        size = len(results)
        if (size > 0):
            pick = random.randint(0, size-1)
            return results[pick]
        else:
            num_defaults = len(self.templates["default"])
            pick = random.randint(0, num_defaults-1)
            return " ".join(self.templates["default"][pick].pattern)

    # TODO
    def ChangeTense(self, verb, words_before, tense="VB"):
        if len(words_before) == 0:
            return verb
        last_phrase = words_before[-1]

        if last_phrase in modal_verb_list:
            return verb

        if re.match(".*and.*", last_phrase):
            tag = u'NNS'
        else:
            doc = self.nlp(last_phrase)
            token = doc[-1]
            tag = token.tag_
        last_phrase = last_phrase.lower()
        transformed_verb = verb
        if tense == "VB" or tense == "VPB" or tense == "VPZ":
            transformed_verb = utility.to_present_tense(tag, last_phrase, verb)
        elif tense == "VBD":
            transformed_verb = utility.to_past_tense(tag, last_phrase,verb)

        return transformed_verb

    def parseNLGData(self):
        for intent in self.nlg_data["templates"]:
            if intent == "_comment":
                continue
            self.templates[intent] = []
            for template in self.nlg_data["templates"][intent]:
                sen_tem = Sentence_Template(template, self.nlg_data["templates"][intent][template])
                self.templates[intent].append(sen_tem)
        for subtem_type in self.nlg_data["sub-templates"]:
            self.subtemplates[subtem_type] = []
            for subtemplate in self.nlg_data["sub-templates"][subtem_type]:
                sen_tem = Sentence_Template(subtemplate, self.nlg_data["sub-templates"][subtem_type][subtemplate])
                self.subtemplates[subtem_type].append(sen_tem)

    def Realization(self, recipe: NLG_Recipe, template_library):
        """
        Generate sentences based on the recipe"
        Assume each template only has at most one sub-template, which does not contain any sub-template itself
        return a list of tuples, in which the first element is the sentence realized, and the second element is a list
        of missing descriptors, e.g.
        [("realized sentence1", [missing descriptor1, missing descriptor 2,...]), ("realized sentence2", [missing descriptor3, missing descriptor 3,...]), ...]
        """

        if template_library == "templates":
            lib = self.templates
        else:
            lib = self.subtemplates

        results = []
        if recipe.intent not in lib:
            print("Invalid Intent. Intent must be one of: " + " ".join(self.templates.keys()))
            return results

        for template in lib[recipe.intent]:
            valid_template = True
            sentences = [[], []]
            subsentences = []
            final_sentences = []
            sentence_index = 0
            keys = recipe.attributes.keys()
            # check if all the attributes in the template exist in the recipe and their values match
            for attribute in template.attributes:
                if attribute not in keys or template.attributes[attribute] != recipe.attributes[attribute]:
                    valid_template = False
                    break
            if not valid_template:
                continue
            keys = set(keys)
            missing_attributes = keys - set(template.attributes)
            keys = recipe.contents.keys()
            for content in template.contents:
                if content not in keys:
                    valid_template = False
                    break
            if not valid_template:
                continue
            keys = set(keys)
            missing_contents = keys - template.contents
            for descriptor in template.descriptors:
                if descriptor not in recipe.descriptors:
                    valid_template = False
                    break
            if not valid_template:
                continue
            missing_descriptors = set(recipe.descriptors) - template.descriptors
            if template_library == "templates":
                if len(missing_attributes) > 0 or len(missing_contents) > 0:
                    if (not template.hasSubtemplate):
                        continue
            else:
                if template.hasSubtemplate:
                    print("Found an invalid sub-template that itself has a sub-template: " + " ".join(template.pattern))
                    continue
            for token in template.pattern:
                match = content_prog.match(token)
                if match:
                    match1 = verb_prog.match(token)
                    if match1:
                        verb = self.ChangeTense(recipe.contents[verb], sentences[sentence_index], recipe.tense)
                        sentences[sentence_index].append(verb)
                    else:
                        sentences[sentence_index].append(recipe.contents[match.group(1)])
                    continue

                match = descriptor_prog.match(token)
                if match:
                    sentences[sentence_index].append(recipe.descriptors[match.group(1)])
                    continue
                match = subtemplate_prog.match(token)
                if match:
                    sub_recipe = NLG_Recipe(match.group(1))
                    sub_contents = {k: content for k, content in recipe.contents.items() if k in missing_contents}
                    sub_recipe.AddContents(sub_contents)
                    for attribute in missing_attributes:
                        sub_recipe.AddAttribute(attribute, recipe.attributes[attribute])
                    for descriptor in missing_descriptors:
                        sub_recipe.AddDescriptor(descriptor, recipe.descriptors[descriptor])
                    subsentences = self.Realization(sub_recipe, "sub-templates")
                    sentence_index = 1
                    continue
                sentences[sentence_index].append(token)
            begin_sentence = " ".join(sentences[0])
            if template_library != "templates":
                final_sentences.append((begin_sentence, missing_descriptors))
            else:
                if template.hasSubtemplate:
                    end_sentence = " ".join(sentences[1])
                    for subsentence in subsentences:
                        complete_sentence = begin_sentence + " " + subsentence[0] + " " + end_sentence
                        for descriptor in subsentence[1]:
                            complete_sentence += " " + recipe.descriptors[descriptor]
                        final_sentences.append((complete_sentence, set()))
                else:
                    complete_sentence = begin_sentence
                    for descriptor in missing_descriptors:
                        complete_sentence += " " + recipe.descriptors[descriptor]
                    final_sentences.append((complete_sentence, set()))
            results.extend(final_sentences)
        return results





        #for template_name in self.templates:
            #if (self.templates[template_name].is_compatible(recipe)):
                #results.extend(self.templates[template_name].generate(self, recipe))
        #return self.SelectResult(recipe, results)