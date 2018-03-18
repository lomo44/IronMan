from Trainer import Trainer
from pprint import pprint
import json
import urllib.parse
import Logic
import spacy

def test_loading():
    data = json.load(open('kb.json'))
    return data

def test_msg(msg):
    access_token = 'L6BRA7QWWZJZK2LGAS7E3EPIMSB22R7D'
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

def play_spacy():
    nlp = spacy.load('en')
    doc = nlp(u'Do you like green flowers?')
    
    for token in doc:
        print(token.text, token.lemma_, token.dep_, token.tag_,
          [child for child in token.children])

    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

def test_kb():
    logic = Logic.Logic('kb.json')
    SELF = logic.kb.get_node('SELF')
    name = logic.kb.get_node('name')
    pprint(logic.kb.bridge(SELF, name))

def test_logic():
    logic = Logic.Logic('kb.json')
    msg = u'Do you like green flowers?'

    # msg = u'who is your father?'
    wit_recipe = test_msg(msg)
    real_recipe = logic.posproc(wit_recipe)

    pprint(real_recipe)

    # resp = logic.respond(wit_recipe)
    # pprint(resp)

if __name__ == "__main__":
    # msg = u'who is your father?'
    # pprint(test_msg(msg))
    # test_logic()
    play_spacy()

    # fill_nbr()