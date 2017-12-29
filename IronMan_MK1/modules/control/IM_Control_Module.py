from IronMan_MK1.modules.base.base_module import Base_module
from IronMan_MK1.modules.base.base_packet import ePacket_flag
from IronMan_MK1.modules.base.fb_packet import FB_packet
from IronMan_MK1.modules.base.converse_context import Converse_context
from IronMan_MK1.modules.base.personality_context import Personality_context,get_default_ironman_context

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
        """
        Get the debug stages of the whole application
        """
        return self.debug_enable

    def process_input(self, _input: FB_packet):
        """
        Handle all of the input related activities
        """
        # check if the participant already in the context
        participant_ID = _input.get_sender_id()
        if participant_ID not in self.contexts_list:
            # converse context does not exist, create a new one
            self.contexts_list[participant_ID] = Converse_context(get_default_ironman_context(), Personality_context())
        # append the packet to the corresponding context
        self.contexts_list[participant_ID].append_packet(_input)

    def process_debug(self, _input: FB_packet):
        """
        Handle all of the debug input from fb packet
        """
        if _input.get_text() == "debug/debug_enable":
            self.debug_enable = True
        if _input.get_text() == "debug/debug_disable":
            self.debug_enable = False
            
    def get_converse_context_from_particiant_ID(self, FB_ID) -> Converse_context:
        """
        Based on the FB id, get the corresponding converse context
        """ 
        if FB_ID in self.contexts_list:
            return self.contexts_list[FB_ID]
        else:
            return None    
    def get_contexts(self):
        '''
        Return all of the stored converse context
        '''
        return self.contexts_list