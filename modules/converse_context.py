import uuid

class converse_context(object):
    def __init__(self):
        self.converse_id = uuid.uuid1()
        self.history_input = []
        pass