# NLG recipe class, used for generate sentence in nlg

from IronMan_MK1.modules.base.decision_vector import Decision_Vector
from typing import List



class NLG_Recipe(object):
    def __init__(self):
        self.objects = []
        self.subjects = []
        self.verbs = "be"
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
        self.verb = verb
        self.requirement["[verb]"] = True
    def get_subjects(self):
        return self.subjects
    def get_objects(self):
        return self.objects
    def get_verb(self):
        return self.verb
    def get_requirement(self):
        return self.requirement
    def generate_subjects(self):
        """
        generate a clause of all the subjects
        for example
        ["I"] returns "I"
        ["you","I"] and ["I","you"] return "you and I"
        ["Mary","you","I"] and ["Mary","I","you"] return "Mary, you and I"
        """
        if not self.requirement["[subject]"]:
            return None
        size = len(self.subjects)
        if size==1:
            return self.subjects[0]

        clause = ""
        foundI = False
        for i, subject in enumerate(self.subjects):
            if i==0:
                if subject!="I":
                    clause += subject
                else:
                    foundI=True
            elif i == size-1:
                if not foundI:
                    clause += " and " + subject
                elif clause == "":
                    clause = subject + " and I"
                else:
                    clause += ", "+subject + " and I"
            else:
                if subject != "I":
                    if clause == "":
                        clause += subject
                    else:
                        clause += ", " + subject
                else:
                    foundI = True
        return clause
    def generate_objects(self):
        """
        generate a clause of all the objects
        for example
        ["me"] returns "me"
        ["her","me"] and ["me","her"] return "her and me"
        ["Mary, "her","me"] and ["me","Mary","her"] return "Mary, her and me"
        """
        if not self.requirement["[object]"]:
            return None
        size = len(self.objects)
        if size==1:
            return self.objects[0]

        clause = ""
        foundMe = False
        for i, object in enumerate(self.objects):
            if i==0:
                if object != "me":
                    clause += object
                else:
                    foundMe = True
            elif i == size-1:
                if not foundMe:
                    clause += " and " + object
                elif clause == "":
                    clause += object + " and me"
                else:
                    clause += ", "+object + " and me"
            else:
                if object != "me":
                    if clause == "":
                        clause += object
                    else:
                        clause += ", " + object
                else:
                    foundMe = True
        return clause
    def generate_verb(self):

        return self.verb()