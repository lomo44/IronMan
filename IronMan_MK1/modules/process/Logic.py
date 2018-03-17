# import intersectiontools as it
import json
import spacy
from pprint import pprint
import re
# import csv
# import parse
import numpy as np
# from pprint import pprint
# from copy import deepcopy

class KnowledgeBase:
    def __init__(self, file):
        data = json.load(open(file))
        self.verify(data)
        self.map = data
        self.gen_anchor()

    def verify(self, map_data):
        for i, n in enumerate(map_data):
            assert n['indx'] == i, 'Invalid Map Data: Indexing'
            for indx in n['NBR']:
                assert i in map_data[indx]['NBR'], 'Invalid Map Data: NBR Pairing'

    def gen_anchor(self):
        anchor = {}
        for node in self.map:
            nname = node['id']
            indx = node['indx']
            try:
                anchor[nname].append(indx)
            except:
                anchor[nname] = [indx]
        self.anchor = anchor


#     def add_node(self, name, content=None, neighbours=None):
#         newNode = _Node(name, content)
#         try:
#             print('add_node: Node already exists: {' + name + ': ' + self._anchor[name] + '}')
#         except:
#             self.anchor[name] = newNode
#             self.map[newNode] = neighbours if neighbours != None else set()

#     def add_edge(self, name_pair):
#         try:
#             node1 = self.anchor[name_pair[0]]
#             node2 = self.anchor[name_pair[1]]
#             self.map[node1].add(node2)
#             self.map[node2].add(node1)
#         except:
#             print('add_edge: Node does not exist: {' + name_pair[0] + ' and/or ' + name_pair[1] + '}')

    def get_node(self, name):
        try:
            return self.map[self.anchor[name][0]]
        except:
            print('node_with_name: Node does not exist: {' + name + "}")

    def get_nbr(self, node):
        return [self.map[i] for i in node['NBR']]

    def bridge(self, node1, node2):

        neig1 = set(node1['NBR'])
        neig2 = set(node2['NBR'])
        return [self.map[i] for i in neig1.intersection(neig2)]

    def walk(self, path):
        #path: list of node names in string
        path = [p for p in path]
        end = self.get_node(path.pop(0))
        for name in path:
            nbr = self.get_nbr(end)
            for n in nbr:
                if name == n['id']:
                    end = n
        return end


class Logic:

    def __init__(self, file, name=None):
        self.name = name
        self.kb = KnowledgeBase(file)
        self.nlp = spacy.load('en')

    def extract(self, entities, key):
        ans = []
        try:
            entity = entities[key]
            for entry in entity:
                ans.append(entry['value'])
            return ans
        except:
            return ans

    def get_poss_chain(self, tokens):
        chain = []
        for token in tokens:
            if token.dep_ == 'poss':
                chain.append(token.text)
        return chain

    def get_tense(self, tokens):
        pos = [token.tag_ for token in tokens]
        return 'VBD' if 'VBD' in pos else 'VB'

    def lemmanize(self, subject):
        return [self.nlp(s)[0].lemma_ for s in subject]

    def remmap(self, poss):
        return [re.sub(r'(?<=^)(you|your)(?=$)', 'SELF', p) for p in poss]

    def posproc(self, recipe):
        text = recipe['_text']
        entities = recipe['entities']
        doc = self.nlp(text)

        rrecipe = {}
        c_type = self.extract(entities, 'c_type')
        subj = self.lemmanize(self.extract(entities, 'subject'))
        pref = self.extract(entities, 'preference')
        chain = self.remmap(self.get_poss_chain(doc))
        tense = self.get_tense(doc)

        def add_to_recipe(content, name):
            for i, c in enumerate(content):
                if len(c) != 0:
                    rrecipe[name[i]] = c

        add_to_recipe(
            [c_type, subj, chain, tense, pref], 
            ['c_type', 'subj', 'poss', 'tense', 'pref']
            )

        return rrecipe

    def pick(self, things):
        np.random.shuffle(things)
        return things.pop()

    def respond(self, recipe):
        recipe = self.posproc(recipe)
        keys = recipe.keys()
        c_type = recipe['c_type']
        subj = [self.kb.get_node(s) for s in recipe['subj']]

        if c_type == 'greeting':
            return recipe

        # if 'pref' in keys:
        #     pref = recipe['pref']
        #     if pref == 'favorite':
        #         cat = self.get_cat(subj)
        #         answer = self.like(cat)
        #     elif pref == 'like':
        #         answer = np.average(self.like(subj))
                
        else:
            if 'poss' in keys:
                poss = recipe['poss']
                start = self.kb.walk(poss)
            elif len(subj) == 2:
                start = subj.pop()

        answer = self.pick(self.kb.bridge(start, subj.pop()))
        recipe['answer'] = answer['id']

            
        return recipe