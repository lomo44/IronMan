import unittest

from processors.echo_processor import echo_processor

from modules.event_loop_module import event_loop_module


class test_echo_process(unittest.TestCase):
    def setUp(self):
        self.event_loop = event_loop_module(echo_processor())
    def test_echo(self):
        return NotImplemented
        #self.event_loop.start()



if __name__ == "__main__":
    unittest.main()