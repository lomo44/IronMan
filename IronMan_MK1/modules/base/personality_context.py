import uuid
import copy

class personality_context():
    def __init__(self):
        self.attribute_dict = {
            "memory_ability" : 100
        }
        self.identifier = uuid.uuid1()
        self.known_personal_context = {}
    def get_memory_ability(self):
        return self.attribute_dict["memory_ability"]
    def get_identifier(self):
        return self.identifier
    def get_deepcopy(self):
        """ 
        return a deep copy of the personality context
        """
        return copy.deepcopy(self)

    def add_known_personal_context(self, personality):
        self.known_personal_context[personality.get_identifier()] = personality.get_deepcopy()
        
    def update_known_personal_context(self, personality):
        if personality.get_identifier() in self.known_personal_context:
            self.known_personal_context[personality.get_identifier()].attribute_dict = personality.attribute_dict
    

