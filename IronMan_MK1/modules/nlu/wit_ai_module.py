from wit import Wit
import requests
from collections import namedtuple

wit_ai_context = namedtuple("wit_ai_context",['client_token','server_token'])


class wit_ai_module(object):
    def __init__(self, input_context:wit_ai_context):
        self.wit_ai_context = input_context
        self.wit_ai_client = Wit(wit_ai_context.client_token)
    def send_message(self, msg):
        return self.wit_ai_client.message(msg)
    def get_all_entities(self):
        header_1 = {
            "Authorization": "Bearer " + self.wit_ai_context.server_token
        }
        reponse = requests.get('https://api.wit.ai/entities', headers=header_1)
        return reponse.json()
    def get_entity_values(self, entity):
        header_1 = {
            "Authorization": "Bearer " + self.wit_ai_context.server_token
        }
        reponse = requests.get('https://api.wit.ai/entities/'+entity, headers=header_1)
        return reponse.json()