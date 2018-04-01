from pprint import pprint
import json
import urllib.parse
from IronMan_MK1.modules.process.Logic import Logic
import spacy
import sys
import os
import string

sys.path.insert(0, '../../../')

from IronMan_MK1.modules.nlg import IM_NLG_Module
from IronMan_MK1.modules.nlu.wit_ai.Trainer import Trainer

SPACY_MODULE_NAME = r"en_core_web_sm"
nlp = spacy.load(SPACY_MODULE_NAME)
def test_loading():
    data = json.load(open('kb.json'))
    return data

def test_wit(msg):
    access_token = 'PGV3XK5N7W7VX6YLPRGZKN7QPXKMLD2W'
    client = Trainer(access_token=access_token)
    msg = msg.lower()

    url = urllib.parse.quote(msg, safe='/', encoding=None, errors=None)
    nlu_resp = client.get_message(url)
    return nlu_resp

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
            print(test_pipe(line), file=write)
            print('', file=write)

# def test_msg(msg, debug=False):
#     logic = Logic.Logic('IronMan_MK1/modules/process/kb.json')
#     return logic.rootproc(msg)

def test_conv():

    logic = Logic('IronMan_MK1/modules/process/kb.json',nlp)
    nlg = IM_NLG_Module.IM_NLG_Module(nlp)
    while True:
        msg = input(': ')
        wit_recipe = test_wit(msg)
        logic_recipe = logic.try_respond(wit_recipe)
        print(nlg.process(logic_recipe))

def test_pipe(msg, debug=False):
    logic = Logic('IronMan_MK1/modules/process/kb.json',nlp)
    wit_recipe = test_wit(msg)
    wit_recipe['_text'] = msg
    logic_recipe = logic.try_respond(wit_recipe, debug=debug)
    nlg = IM_NLG_Module.IM_NLG_Module(nlp)
    return nlg.process(logic_recipe)

if __name__ == "__main__":
    os.chdir('../../../')
    if 'conv' in sys.argv:
        test_conv()
    elif 'file' in sys.argv:
        decomp_file('IronMan_MK1/modules/process/questions', 'IronMan_MK1/modules/process/answers')
    else:
        msg = u'What is your name?'
        # play_spacy(msg)
        print(test_pipe(msg, True))
    

