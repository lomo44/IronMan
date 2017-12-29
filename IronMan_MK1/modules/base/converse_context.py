import uuid
from IronMan_MK1.modules.base.personality_context import Personality_context
from IronMan_MK1.modules.base.fb_packet import FB_packet
from queue import Queue
from collections import deque

class Converse_context(object):
    def __init__(self, characterA: Personality_context, characterB: Personality_context):
        """
        Initialize a converse context
        characterA: Main character, this personality context should be our iron man
        characterB: secondary character, this personality context should be our user
        unprocessed_msg: A deque that used for storing the pure incomming message (Raw text)
        unprocessed_comp: A deque that store incomming NLU composition after the the raw text has been analyzed by the NLU for processing
        unprocessed_recipes: A deque that consits the output nlg generation recipe after processing
        unprocessed_responses: A deque that consists of the pure raw text that should be post to the front end
        """
        self.ID = uuid.uuid1()
        self.last_active_timestamp = None
        self.history_converse_packets = []

        # and known character context for each other
        characterA.add_known_personal_context(characterB)
        characterB.add_known_personal_context(characterA)
        self.characterA = characterA
        self.characterB = characterB
        self.unprocessed_msg = deque()
        self.unprocessed_comp = deque()
        self.unprocessed_recipes = deque()
        self.unprocessed_responses = deque()
    
    def get_unprocessed_msg_deque(self) -> deque:
        """
        Return the unprocessed message deque of this context
        """
        return self.unprocessed_msg

    def get_unprocessed_recipes_deque(self) -> deque:
        """
        Return the unprocessed recipes deque. This deque is used for storing the unprocesed information after the 
        processing stage. Recipe is used for NLG
        """
        return self.unprocessed_recipes

    def get_unprocessed_response_deque(self) -> deque:
        """
        Return the unprocessed response deque. This deque consists the unsent response after NLG.
        """
        return self.unprocessed_responses


    def update_personality_contexts(self,characterA:Personality_context, characterB:Personality_context):
        characterA.update_personality_contexts(characterB)
        characterB.update_personality_contexts(characterA)

    def get_id(self):
        """
        Return the context ID
        """
        return self.ID

    def get_participants_latest_msg(self,participants_id):
        """
        Iterate through the memory packet, find the latest msg for that participants
        """
        for packet in self.history_converse_packets:
            if packet.get_sender_id() == participants_id:
                return packet.get_text()
        return None
    
    def append_packet(self, new_packet: FB_packet):
        # append historical packets
        self.history_converse_packets.append(new_packet)
        # grab the text and put it in the unprocessed deque
        self.unprocessed_msg.append(new_packet.get_text())