from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http.response import HttpResponse
import json
from pprint import pprint
import requests
import urllib.parse
import sputnik
import spacy.about
from IronMan_MK1.modules.nlu.wit_ai.Trainer import Trainer
from IronMan_MK1.modules.process.Logic import Logic
from IronMan_MK1.modules.nlg.IM_NLG_Module import IM_NLG_Module
# Create your views here.

# Launch script to install spacy's english module.
# package = sputnik.install('spacy', spacy.about.__version__, spacy.about.__default_model__)

FB_VERIFICATION_TOKEN = 'ece496'
FB_PAGE_ACCESS_TOKEN = r'EAAWlbODcLv0BAHQu707XLzZAxoPIvluEX12pvADWuXIv2dd5qIYtqIYNZC67k5DrtYnSWdumHLiEjnliw0odaZBH48XXKu3ILViPAZAaSvLfyUS5ikOPWsIWagLgh6N5eoFKbfoZAaO50Jc1DiSwc0f8KKilpqKrZAPsBld1eqhkPtlF5PeKbt'
WIT_AI_ACCESS_TOKEN = r'PGV3XK5N7W7VX6YLPRGZKN7QPXKMLD2W'
LOGIC_BASE_PATH = r'IronMan_MK1/modules/process/kb.json'
NLG_BASE_PATH  =r'IronMan_MK1/modules/nlg/iron_man_data2.json'
SPACY_MODULE_NAME = r'en_core_web_sm'

spacy_module = spacy.load(SPACY_MODULE_NAME);
witAITrainer = Trainer(access_token = WIT_AI_ACCESS_TOKEN)
logicModule = Logic(LOGIC_BASE_PATH,spacy_module, name=None)
nlgModule = IM_NLG_Module(spacy_module,json_file=NLG_BASE_PATH)


def processNLU(msg):
    msg = msg.lower()
    url = urllib.parse.quote(msg, safe='/', encoding=None, errors=None)
    nlu_resp = witAITrainer.get_message(url)
    return nlu_resp

def processLogic(recipe):
    return logicModule.try_respond(recipe)

def processNLG(logic_recipe):
    return nlgModule.process(logic_recipe)

def post_fb_messager_msg(fbid, received_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(FB_PAGE_ACCESS_TOKEN)
    print(post_message_url)
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": received_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())





class fb_echo(generic.View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)


    def get(self, request, *args, **kwargs):

        # token verification
        if self.request.GET['hub.verify_token'] == FB_VERIFICATION_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

        return HttpResponse("Hello world")

    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    if 'text' in message['message']:
                        msg = message['message']['text']
                        wit_recipe = processNLU(msg)
                        logic_recipe = processLogic(wit_recipe)
                        output = processNLG(logic_recipe)
                        post_fb_messager_msg(message['sender']['id'],output)
                    else:
                        post_fb_messager_msg(message['sender']['id'],"Invalid Input")
                    # if 'text' in message['message']:
                    #     if message['message']['text'] == 'mike is stupid':
                    #         post_fb_messager_msg(message['sender']['id'],"No, he is smart")
                    #     else:
                    #         post_fb_messager_msg(message['sender']['id'], message['message']['text'])
                    # else:
                    #     post_fb_messager_msg(message['sender']['id'], "Image/Gif support is limited")
        return HttpResponse()
