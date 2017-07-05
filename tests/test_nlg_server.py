import unittest
from nlg_module import nlg_module
import time


class test_nlg_module_basic(unittest.TestCase):
    def setUp(self):
        self.host_name = "localhost"
        self.host_port = 8080

    def test_start_server(self):
        new_nlg_module = nlg_module()
        new_nlg_module.start_server(self.host_name, self.host_port)
        self.assertTrue(new_nlg_module.server_started)
        new_nlg_module.stop_server()

    def test_end_server(self):
        new_nlg_module = nlg_module()
        new_nlg_module.start_server(self.host_name, self.host_port)
        new_nlg_module.stop_server()
        self.assertFalse(new_nlg_module.server_started)


class test_nlg_module_tense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host_name = "localhost"
        cls.host_port = 8080
        cls.nlg = nlg_module()
        cls.nlg.start_server(cls.host_name, cls.host_port)
        cls.sentence = {}
        cls.sentence["subject"] = "John"
        cls.sentence["verb"] = "kick"
        cls.sentence["object"] = "Dave"

    @classmethod
    def tearDownClass(cls):
        cls.nlg.stop_server()

    def test_present_tense(self):
        self.sentence["features"] = {"tense": "present"}
        self.assertEqual(self.nlg.send_data(self.sentence), "John kicks Dave.")

    def test_pass_tense(self):
        self.sentence["features"] = {"tense": "past"}
        self.assertEqual(self.nlg.send_data(self.sentence), "John kicked Dave.")

    def test_future_tense(self):
        self.sentence["features"] = {"tense": "future"}
        self.assertEqual(self.nlg.send_data(self.sentence), "John will kick Dave.")


if __name__ == "__main__":
    unittest.main()
