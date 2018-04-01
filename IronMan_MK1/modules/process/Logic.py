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
        np.random.seed()
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
        try:
            return self.map[self.anchor[name.upper()][0]]
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

    def __init__(self, file, nlp, name=None):
        self.name = name
        self.kb = KnowledgeBase(file)
        self.nlp = nlp
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

    def pick(self, things):
        np.random.shuffle(things)
        return things.pop() if len(things) > 0 else None

    def like(self, nodes):
        likeness = []
        for n in nodes:
            if 'likeness' in n.keys():
                likeness.append(n['likeness'])
            elif n['cat'] == 'TOP':
                likeness.append(np.average(self.like(self.kb.get_nbr(n))))
            else:
                likeness.append(6)

        return likeness

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

    #*************FUCK WIT AI****************
    def rootproc(self, msg):
        doc = self.nlp(msg)

        tokens = [token for token in doc]
        dep_ = [token.dep_ for token in doc]
        

        if 'compound' in dep_:
            comp_idx = dep_.index('compound')
            comp_an = tokens.pop(comp_idx + 1)
            new_words = []
            for i, token in enumerate(tokens):
                if i == comp_idx:
                    new_words.append(token.text + ' ' + comp_an.text)
                else:
                    new_words.append(token.text)

            doc = spacy.tokens.Doc(self.nlp.vocab, words=new_words)
            doc = self.nlp.parser(doc)
            tokens = [token for token in doc]
            dep_ = [token.dep_ for token in doc]

        stop = list(string.punctuation) + ['do', '\'s', 'a']
        chains = []

        root_idx = dep_.index('ROOT')
        root = tokens[root_idx]
        root_children = [child for child in root.children if child.lemma_.lower() not in stop]
        for head in root_children:
            chain = []

            def build_dep(child):
                for c in [asdasd for asdasd in child.children if asdasd.lemma_.lower() not in stop]:
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

    def test_spacy(self, msg, file=None):
        doc = self.nlp(msg)
        
        for token in doc:
            print(token.text, token.lemma_, token.dep_, token.tag_,
              [child for child in token.children], file=file)

    def norm(self, token):
        if type(token) is str:
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
            elif name == 'identity':
                nbr = self.kb.get_nbr(end)
                for n in nbr:
                    if 'name' == n['cat'] or 'relationship' == n['cat']:
                        end = n
                        break
                break
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
        if string in node['id'].lower():
            return True, node
        else:
            for nbr in self.kb.get_nbr(node):
                if string in nbr['id'].lower():
                    return True, nbr
        return False, None

    def read_chain(self, chain):
        path = [self.norm(token) for token in chain]
        result = self.walk(path)
        return result

    def get_topic(self, chain):
        top = []
        for word in chain:
            if type(word) is str:
                continue
            elif word.text.lower() == 'you':
                top.append('I')
            elif word.text.lower() == 'your':
                top.append('my')
            elif word.dep_ == 'poss':
                top.append(word.text + '\'s')
            else:
                top.append(word.text)
        return ' '.join(top)

    def try_respond(self, recipe, debug=False):
        response = {}

        msg = recipe['_text']
        entities = recipe['entities']
        if 'greetings' in entities.keys():
            response['intent'] = 'greetings'
            return response
        
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

        if debug:
            self.test_spacy(msg)
            print('')
            print(chains, '\n')

        if root.lemma_ == 'be':
            response['intent'] = 'information'

            lead = chains.pop(0)
            lead_str = ' '.join([l.lemma_.lower() for l in lead])
            if lead[0].lemma_.lower() in intent_map.keys():
                head = lead.pop(0)
                intent = intent_map[head.lemma_.lower()]
                if len(lead) == 0 and intent != 'general':
                    chains[0].append(intent)
                else:
                    chains[0] += lead
            elif lead_str in intent_map.keys():
                intent = intent_map[lead_str]
                chains[0].append(intent)
            else:
                chains.insert(0, lead)
            if debug:
                print(chains, '\n')

            if len(chains) == 1:
                answer = self.read_chain(chains[0])
                contents = {}
                if np.random.ranf() > 0.3:
                    contents['topic'] = self.get_topic(chains[0])

                content = answer['id']

                #WARN SELF is the only identity at this point
                if answer['cat'] == 'relationship':
                    content = 'my ' + content

                contents['content'] = content
                response['contents'] = contents
                description = self.describe(answer)

                testf = np.random.ranf()
                if description is not None and testf > 0:
                    response['descriptions'] = {'description' : description}

            elif len(chains) == 2:
                answer = self.read_chain(chains[0])
                asser, v_answer = self.verify(answer, ' '.join([c.lemma_ for c in chains[1]]))
                response['assertion'] = asser

                contents = {}
                if np.random.ranf() > 0.65 and asser:
                    contents['topic'] = self.get_topic(chains[0])
                    contents['content'] = v_answer['id']
                    response['contents'] = contents
                    description = self.describe(v_answer)
                    if description is not None:
                        response['descriptions'] = {'description' : description}

        if root.lemma_ == 'like':
            response['intent'] = 'preference'
            for i, chain in enumerate(chains):
                print(chain)
                if len(chain) == 1 and chain[0].text.lower() == 'you':
                    chains.pop(i)
                    break

            if len(chains) == 1:
                path = [self.norm(c) for c in chains[0]]
                nodes = [self.kb.get_node(p) for p in path]

                likeness = np.average(self.like(nodes))
                response['assertion'] = likeness > 7
                contents = {}

                if np.random.ranf() > 0.25:
                    contents['content'] = self.get_topic(chains[0])
                    response['contents'] = contents

                last_node = self.kb.get_node(path[-1])
                description = self.describe(last_node)

                if description is not None:
                    response['descriptions'] = {'description' : description}

        if debug:
            print(response,'\n')

        return response
        