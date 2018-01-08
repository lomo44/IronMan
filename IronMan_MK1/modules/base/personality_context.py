import uuid
import copy

class Personality_context():
    def __init__(self):
        self.attribute_dict = {
            "memory_ability" : 100
        }
        self.id = uuid.uuid1()
        self.known_personal_context = {}
    def get_memory_ability(self):
        return self.attribute_dict["memory_ability"]
    def get_id(self):
        return self.id
    def get_deepcopy(self):
        """ 
        return a deep copy of the personality context
        """
        return copy.deepcopy(self)

    def add_known_personal_context(self, personality):
        self.known_personal_context[personality.get_id()] = personality.get_deepcopy()
        
    def update_known_personal_context(self, personality):
        if personality.get_id() in self.known_personal_context:
            self.known_personal_context[personality.get_id()].attribute_dict = personality.attribute_dict
    

def get_default_ironman_context_id():
    """
    Return the default iron man personality id
    """
    return "Iron_Man"

def get_default_ironman_context() -> Personality_context:
    """
    Generate the initial stage of the iron man personality
    Current stage is very limited. We need to add more traits
    """
    ironman = Personality_context()
    ironman.id = "Iron_Man"
    return ironman