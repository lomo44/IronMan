import json

class fb_packet(object):
    def __init__(self):
        self.json = {
            'entry':{
            'messaging' : {
                'sender' : {
                    'id' : 'TEST_FB_ID'
                },
                'text' : ""
                }
            }
        }
    def __str__(self):
        return json.dumps(self.json,indent=4)
    def set_sender_id(self, sender_id):
        self.json['entry']['messaging']['sender']['id'] = sender_id
    def set_text(self,text):
        self.json['entry']['messaging']['text'] = text
    def get_sender_id(self):
        return self.json['entry']['messaging']['sender']['id']
    def get_text(self):
        return self.json['entry']['messaging']['text']
    @staticmethod
    def initialize_from_json(input_json):   
        ret_obj = fb_packet()
        ret_obj.json = input_json
        return ret_obj
    @staticmethod
    def generate_mock_packet(sender_id,message):
        
        ret_obj = fb_packet()
        ret_obj.set_sender_id(sender_id)
        ret_obj.set_text(message)
        return ret_obj
