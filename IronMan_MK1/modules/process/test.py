from pprint import pprint
import json
import urllib.parse
import Logic
import spacy
import sys
import os
import string

sys.path.insert(0, '../../../')

from IronMan_MK1.modules.nlg import IM_NLG_Module
from IronMan_MK1.modules.nlu.wit_ai.Trainer import Trainer

def test_loading():
    data = json.load(open('kb.json'))
    return data

# def test_msg(msg):
#     access_token = 'L6BRA7QWWZJZK2LGAS7E3EPIMSB22R7D'
#     client = Trainer(access_token=access_token)
#     msg = msg.lower()

#     url = urllib.parse.quote(msg, safe='/', encoding=None, errors=None)
#     nlu_resp = client.get_message(url)
#     return nlu_resp

def add_indx():
    data = json.load(open('kb.json'))
    for i, n in enumerate(data):
        n['indx'] = i
    with open('kb.json', 'w') as out:
        json.dump(data, out, indent=4, sort_keys=True)

def fill_nbr():
    data = json.load(open('kb.json'))
    for i, n in enumerate(data):
        assert(n['indx'] == i)
        if 'NBR' not in n.keys():
            n['NBR'] = []
    for i, n in enumerate(data):
        try:
            for indx in n['NBR']:
                data[indx]['NBR'].append(i) if i not in data[indx]['NBR'] else None
        except:
            None
    with open('kb.json', 'w') as out:
        json.dump(data, out, indent=4, sort_keys=True)

def test_print_NBRs():
    data = json.load(open('kb.json'))
    for i, n in enumerate(data):
        assert(n['indx'] == i)
        nbrs = [data[indx]['id'] for indx in n['NBR']]
        print(n['id'], nbrs)

def play_spacy(msg, file=None):
    nlp = spacy.load('en')
    doc = nlp(msg)
    
    for token in doc:
        print(token.text, token.lemma_, token.dep_, token.tag_,
          [child for child in token.children], file=file)

    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_m, file=file)

def test_kb():
    logic = Logic.Logic('IronMan_MK1/modules/process/kb.json')
    SELF = logic.kb.get_node('SELF')
    name = logic.kb.get_node('name')
    pprint(logic.kb.bridge(SELF, name))

def test_logic(msg):
    logic = Logic.Logic('IronMan_MK1/modules/process/kb.json')
    wit_recipe = test_msg(msg)
    real_recipe = logic.posproc(wit_recipe)

    # pprint(real_recipe)

    resp = logic.respond(wit_recipe)
    return resp


def decomp_file(input, output):
    with open(input, 'r') as read, open(output, 'w') as write:
        logic = Logic.Logic('IronMan_MK1/modules/process/kb.json')
        data = read.readlines()
        lines = [d.strip() for d in data]
        for line in lines:
            print(line, file=write)
            # logic.test_spacy(line, file=write)
            print(logic.rootproc(line), file=write)
            print('', file=write)

def test_msg(msg):
    logic = Logic.Logic('IronMan_MK1/modules/process/kb.json')
    return logic.try_respond(msg)

if __name__ == "__main__":
    os.chdir('../../../')
<<<<<<< HEAD
    msg = u'Which car is your favorite?'
    # decomp_file('IronMan_MK1/modules/process/questions', 'IronMan_MK1/modules/process/answers')
    
    # test_msg(msg)
    # play_spacy(msg)
    # print(rootproc(msg))

    # pprint(test_msg(msg))
    # pprint(test_logic(msg))
    nlg = IM_NLG_Module.IM_NLG_Module()
    print(nlg.process(test_msg(msg)))
=======
    # nlg = IM_NLG_Module.IM_NLG_Module()
    # print(nlg.process(test_logic()))
    pprint(test_logic())
>>>>>>> 402ae94b3c9648bdfe05a72abcf90b3e710312c1

