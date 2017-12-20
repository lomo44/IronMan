import uuid
from IronMan_MK1.modules.base.personality_context import personality_context

class converse_context(object):
    def __init__(self, characterA: personality_context, characterB: personality_context):
        """
        Initialize a converse context
        characterA: Main character, this personality context should be our iron man
        characterB: secondary character, this personality context should be our user
        """
        self.ID = uuid.uuid1()
        self.last_active_timestamp = None
        self.history_converse_packets = []
        # and known character context for each other
        characterA.add_known_personal_context(characterB)
        characterB.add_known_personal_context(characterA)
        self.characterA = characterA
        self.characterB = characterB

    def update_personality_contexts(self,characterA:personality_context, characterB:personality_context):
        characterA.update_personality_contexts(characterB)
        characterB.update_personality_contexts(characterA)

    def get_id(self):
        return self.ID

    def get_participants_latest_msg(self,participants_id):
        """
        Iterate through the memory packet, find the latest msg for that participants
        """
        for packet in self.history_converse_packets:
            if packet.get_sender_id() == participants_id:
                return packet.get_text()
        return None
    