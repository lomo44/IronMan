from processors import basic_processor


class base_core(object):
    def __init__(self, processor: basic_processor):
        self.processor = processor
        self.command_dict = self.init_command_dict()

    def init_command_dict(self):
        return NotImplemented

    def process_command(self, command):
        if command in self.command_dict:
            self.command_dict[command]()

