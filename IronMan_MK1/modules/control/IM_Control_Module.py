from IronMan_MK1.modules.base.base_module import Base_module
from IronMan_MK1.modules.base.base_packet import Base_packet, ePacket_flag
from IronMan_MK1.modules.base.fb_packet import FB_packet
from IronMan_MK1.modules.base.converse_context import converse_context
from IronMan_MK1.modules.base.personality_context import personality_context,get_default_ironman_context

class IM_Control_Module(Base_module):
    def __init__(self):
        Base_module.__init__(self)
        self.debug_enable = False
        self.contexts_list = {}

    def process(self, _input: FB_packet):
        if _input.type == ePacket_flag.ePacketType_FB:
            # processing information
            self.process_debug(_input)
            self.process_input(_input)

    def get_debug_state(self):
        return self.debug_enable

    def process_input(self, _input: FB_packet):
        # check if the participant already in the context
        participant_ID = _input.get_sender_id()
        if participant_ID not in self.contexts_list:
            self.contexts_list[participant_ID] = converse_context(get_default_ironman_context(),personality_context())
        # append the packet to the corresponding context
        self.contexts_list[participant_ID].append_packet(_input)

    def process_debug(self, _input: FB_packet):
        if _input.get_text() == "debug/debug_enable":
                self.debug_enable = True
        if _input.get_text() == "debug/debug_disable":
                self.debug_enable = False
    
    def get_converse_context_from_particiant_ID(self, participant_ID) -> converse_context:
        if participant_ID in self.contexts_list:
            return self.contexts_list[participant_ID]
        else:
            return None
