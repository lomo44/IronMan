# NLG recipe class, used for generate sentence in nlg

from IronMan_MK1.modules.base.decision_vector import Decision_Vector
from typing import List



class NLG_Recipe(object):
    def __init__(self):
        self.objects = []
        self.subjects = []
        self.verbs = []
        self.attribute = {}
        self.requirement = {
            "[object]" : False,
            "[subject]" : False,
            "[verb]" : False
        }
        #self.decision_vector = Decision_Vector()
        
    def add_subject(self, subject:str):
        """
        Add subject to the recipe
        """
        self.subjects.append(subject)
        self.requirement["[subject]"] = True
    def add_object(self, _object):
        """
        Add object to the recipe
        """
        self.objects.append(_object)
        self.requirement["[object]"] = True
    def add_verb(self, verb):
        """
        Add verb to the recipe
        """
        self.verbs.append(verb)
        self.requirement["[verb]"] = True
    def get_subjects(self):
        return self.subjects
    def get_objects(self):
        return self.objects
    def get_verbs(self):
        return self.verbs
    def get_requirement(self):
        return self.requirement
    # def get_decision_vector(self) -> Decision_Vector:
    #     """
    #     Get the decision vector of the recipe
    #     """
    #     return self.decision_vector