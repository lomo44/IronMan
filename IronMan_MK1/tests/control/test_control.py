import unittest
import sys
import os 
from IronMan_MK1.modules.control.IM_Control_Module import IM_Control_Module
from IronMan_MK1.modules.base.fb_packet import FB_packet

class test_IM_control_module(unittest.TestCase):
    def setUp(self):
        self.control_module = IM_Control_Module()
    def test_enable_debug(self):
        change_mode_packet = FB_packet()
        change_mode_packet.set_text("debug/debug_enable")
        self.control_module.process(change_mode_packet)
        self.assertEqual(self.control_module.get_debug_state(),True)

    def test_disable_debug(self):
        change_mode_packet = FB_packet()
        change_mode_packet.set_text("debug/debug_enable")
        self.control_module.process(change_mode_packet)
        self.assertEqual(self.control_module.get_debug_state(),True, msg="Invalid Enable Stage")
        change_mode_packet.set_text("debug/debug_disable")
        self.control_module.process(change_mode_packet)
        self.assertEqual(self.control_module.get_debug_state(),False,msg="Invalid Disable Stage")

    def test_add_new_participant(self):
        packet = FB_packet()
        packet.set_sender_id("123")
        packet.set_text("msg")
        self.control_module.process(packet)
        converse_context = self.control_module.get_converse_context_from_particiant_ID("123")
        self.assertNotEqual(converse_context,None,msg="Invalid Context")
        self.assertEqual(converse_context.get_participants_latest_msg("123"),"msg")


if __name__ == "__main__":
    unittest.main()