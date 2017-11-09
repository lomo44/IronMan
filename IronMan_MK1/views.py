from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http.response import HttpResponse
import json
from pprint import pprint
import requests
# Create your views here.


FB_VERIFICATION_TOKEN = 'ece496'
FB_PAGE_ACCESS_TOKEN = r'EAAWlbODcLv0BAHQu707XLzZAxoPIvluEX12pvADWuXIv2dd5qIYtqIYNZC67k5DrtYnSWdumHLiEjnliw0odaZBH48XXKu3ILViPAZAaSvLfyUS5ikOPWsIWagLgh6N5eoFKbfoZAaO50Jc1DiSwc0f8KKilpqKrZAPsBld1eqhkPtlF5PeKbt'


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
                    if 'text' in mesasge['mssage']:
                        post_fb_messager_msg(message['sender']['id'], message['message']['text'])
                    else
                        post_fb_messager_msg(message['sender']['id'], "Image/Gif support is limited")
        return HttpResponse()