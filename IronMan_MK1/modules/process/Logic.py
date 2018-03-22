# import intersectiontools as it
import json
import spacy
from pprint import pprint
import re
# import csv
# import parse
import numpy as np
import string
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
        self.intents = [
            'information',
            'identity',
            'time',
            'preference',
            'ability',
            'experience',
            'opinion',
            'initiation',
            'greetings']

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
        return things.pop() if len(things) > 0 else None

    def like(self, nodes):
        return [n['likeness'] for n in nodes if 'likeness' in n.keys()]

    def favorite(self, node):
        nbr = self.kb.get_nbr(node)
        likeness = self.like(nbr)
        return nbr[np.argmax(likeness)]

    def describe(self, node):
        d = []
        for key in node.keys():
            if key in ['opinion', 'experience', 'pause', 'description']:
                np.random.shuffle(node[key])
                d.append(node[key][0])
        return self.pick(d)

    def respond(self, recipe):
        '''
        intent:
            information
            identity
            time
            preference
            ability
            experience
            opinion
            initiation
            greetings
        contents:
            content
            category
            verb
        assertion:
        tense:
        description:
            opinion
            pause
            experience
        '''

        recipe = self.posproc(recipe)

        keys = recipe.keys()
        c_type = recipe['c_type']
        subj = [self.kb.get_node(s) for s in recipe['subj']]

        if c_type == 'greeting':
            return recipe

        response = {}
        contents = {}

        if 'pref' in keys:
            intent = 'preference'
            pref = recipe['pref'][0]
            if pref == 'favorite':
                cat = self.get_cat(subj)
                answer = self.like(cat)
            elif pref == 'like':
                likeness = np.average(self.like(subj))
                answer = self.pick(subj)
                contents['content'] = answer['id']
                response['assertion'] = likeness > .5
                
        else:
            intent = 'information'
            if 'poss' in keys:
                poss = recipe['poss']
                start = self.kb.walk(poss)
            elif len(subj) == 2:
                start = subj.pop()

            answer = self.pick(self.kb.bridge(start, subj.pop()))
        
            contents['content'] = answer['id']
        
        description = self.describe(answer)

        response['intent'] = intent
        response['contents'] = contents
        response['tense'] = recipe['tense']
    
        if description is not None:
            response['description'] = description
            
        return response
    #*************FUCK WIT AI****************
    def rootproc(self, msg):
        # nlp = spacy.load('en')
        doc = self.nlp(msg)

        stop = list(string.punctuation) + ['do', '\'s', 'a']
        
        tokens = [token for token in doc]
        dep_ = [token.dep_ for token in doc]

        chains = []

        root_idx = dep_.index('ROOT')
        root = tokens[root_idx]
        root_children = [child for child in root.children if child.lemma_ not in stop]
        for head in root_children:
            chain = []

            def build_dep(child):
                for c in [asdasd for asdasd in child.children if asdasd.lemma_ not in stop]:
                    if c.dep_ == 'prep':
                        for a in c.ancestors:
                            if a.lemma_ not in stop and a != root:
                                chain.append(a)
                    build_dep(c)
                
                if child not in chain and child.dep_ != 'prep':
                    chain.append(child)


            build_dep(head)
            chains.append(chain)

        

        return {'ROOT' : root, 'chain' : chains}
    
    def proc_intent(self, chains):
        intent_map = {
            'what' : 'general',
            'how' : 'eval',
            'when' : 'time',
            'who' : 'identity',
            'which' : 'reorder',
            'where' : 'location'
        }
        
        chain = chains[0]
        lead = chain[0]

        if lead.lemma_ in intent_map.keys():
            chain.pop(0)
            chains.pop(0)
            intent = intent_map[lead.lemma_]

            if intent == 'reorder':
                chains.append(chain)

            elif intent == 'eval':
                if len(chain) == 0:
                    chains.append([lead])
                elif chain[0].lemma_ == 'old':
                    chains.append(['age'])
                else:
                    chains.append(chain)

            elif intent == 'general':
                if len(chain) != 0:
                    chains.append(chain)

            else:
                chains.append([intent])
        return chains

    def test_spacy(self, msg, file=None):
        doc = self.nlp(msg)
        
        for token in doc:
            print(token.text, token.lemma_, token.dep_, token.tag_,
              [child for child in token.children], file=file)

    def norm(self, token):
        if token is str:
            return token
        elif token.text.lower() == 'your' or token.text.lower() == 'you':
            return 'SELF'
        else:
            return token.lemma_

    def walk(self, path):
        #path: list of node names in string
        path = [p for p in path]
        end = None
        for i, name in enumerate(path):
            if name == 'favorite':
                end = self.favorite(self.walk(path[i+1:]))
                break
            elif name == 'opinion':
                end = self.walk(path[i+1:])
                break
            elif name == 'kind':
                continue
            if end is None:
                end = self.kb.get_node(name)
            else:
                nbr = self.kb.get_nbr(end)
                for n in nbr:
                    if name == n['id']:
                        end = n
                        break
                    elif name == n['cat']:
                        end = n
        return end

    def verify(self, node, string):
        return string in node['id'].lower()

    def read_chain(self, chain):
        path = [self.norm(token) for token in chain]
        result = self.walk(path)
        return result

    def get_topic(self, chain):
        top = []
        for word in chain:
            if word.text.lower() == 'you':
                top.append('I')
            elif word.text.lower() == 'your':
                top.append('my')
            elif word.dep_ == 'poss':
                top.append(word.lemma_ + '\'s')
            else:
                top.append(word.lemma_)
        return ' '.join(top)

    def try_respond(self, msg):
 
        intent_map = {
            'what' : 'general',
            'how old' : 'age',
            'when' : 'time',
            'who' : 'identity',
            'where' : 'location',
            'which' : 'reorder'
        }

        recipe = self.rootproc(msg)
        root = recipe['ROOT']
        chains = recipe['chain']
        self.test_spacy(msg)

        # print('')
        # print(chains, '\n')
        response = {}

        if root.lemma_ == 'be':
            response['intent'] = 'information'

            lead = chains.pop(0)
            lead_str = ' '.join([l.lemma_ for l in lead])
            if lead[0].lemma_ in intent_map.keys():
                head = lead.pop(0)
                intent = intent_map[head.lemma_]
                if len(lead) == 0 and intent != 'general':
                    chains[0].append(intent)
                else:
                    chains[0] += lead
            elif lead_str in intent_map.keys():
                intent = intent_map[lead_str]
                chains[0].append(intent)
            else:
                chains.insert(0, lead)
            if len(chains) == 1:
                answer = self.read_chain(chains[0])
                contents = {}
                contents['topic'] = self.get_topic(chains[0])
                contents['content'] = answer['id']
                response['contents'] = contents
                description = self.describe(answer)

                if description is not None:
                    response['description'] = description

            elif len(chains) == 2:
                answer = self.read_chain(chains[0])
                asser = self.verify(answer, ' '.join([c.lemma_ for c in chains[1]]))
                response['assertion'] = asser

                contents = {}
                contents['topic'] = self.get_topic(chains[0])
                contents['content'] = answer['id']
                response['contents'] = contents
                description = self.describe(answer)

                if description is not None:
                    response['description'] = description


        if root.lemma_ == 'like':
            None

        return response
        