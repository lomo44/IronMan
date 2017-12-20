import uuid
from IronMan_MK1.modules.base.personality_context import personality_context

class converse_context(object):
    def __init__(self, characterA: personality_context, characterB: personality_context):
        self.last_active_timestamp = None
        self.history_converse_packets = []
        # and known character context for each other
        characterA.add_known_personal_context(characterB)
        characterB.add_known_personal_context(characterA)

    def update_personality_contexts(self,characterA:personality_context, characterB:personality_context):
        characterA.update_personality_contexts(characterB)
        characterB.update_personality_contexts(characterA)