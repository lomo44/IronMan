# NLG recipe class, used for generate sentence in nlg

from IronMan_MK1.modules.base.decision_vector import Decision_Vector
from typing import List



class NLG_Recipe(object):
    def __init__(self, intent):
        self.intent = intent
        self.contents = []
        self.attributes = {}
        self.tense = "VB"
        self.descriptors = {}

        
    def AddContents(self, contents):
        """
        Add contents to the recipe
        """
        self.contents.extend(contents)
        self.GenerateIClause()
        self.GenerateMeClause()
        self.GenerateClause()


    def GetContents(self):
        return self.contents

    def AddAttribute(self, attribute, attribute_val):
        self.attributes[attribute] = attribute_val

    def GenerateIClause(self):
        """
        for each content element in self.contents, if a content is still a list (unprocessed),
        then change it into a clause if it has "I" or it has only one element
        for example:
        ["I"] -> "I"
        ["you","I"] and ["I","you"] return "you and I"
        ["Mary","you","I"] and ["Mary","I","you"] return "Mary, you and I"
        ["David", "Mary", "Steven"] -> ["David, Mary and Steven"]
        """
        for i, content in enumerate(self.contents):
            if not isinstance(content, list):
                continue

            if len(content) == 1:
                self.contents[i] = content[0]
                continue

            clause = ""
            foundI = False
            size = len(content)
            for j, elem in enumerate(content):
                if j == 0:
                    if elem!="I":
                        clause += elem
                    else:
                        foundI=True
                elif j == size-1:
                    if not foundI:
                        clause += " and " + elem
                    elif clause == "":
                        clause = elem + " and I"
                    else:
                        clause += ", "+ elem + " and I"
                else:
                    if elem != "I":
                        if clause == "":
                            clause += elem
                        else:
                            clause += ", " + elem
                    else:
                        foundI = True
            if (foundI):
                self.contents[i] = clause

    def GenerateMeClause(self):
        """
        for each content element in self.contents, if a content is still a list (unprocessed),
        then change it into a clause if it has "me" or it has only one element
        for example:
        for example
        ["me"] -> "me"
        ["her","me"] and ["me","her"] -> "her and me"
        ["Mary, "her","me"] and ["me","Mary","her"] -> "Mary, her and me"
        """
        for i, content in enumerate(self.contents):
            if not isinstance(content, list):
                continue

            if len(content) == 1:
                self.contents[i] = content[0]
                continue

            clause = ""
            foundme = False
            size = len(content)
            for j, elem in enumerate(content):
                if j == 0:
                    if elem!="me":
                        clause += elem
                    else:
                        foundme=True
                elif j == size-1:
                    if not foundme:
                        clause += " and " + elem
                    elif clause == "":
                        clause = elem + " and me"
                    else:
                        clause += ", "+ elem + " and me"
                else:
                    if elem != "me":
                        if clause == "":
                            clause += elem
                        else:
                            clause += ", " + elem
                    else:
                        foundme = True
            if (foundme):
                self.contents[i] = clause

    def GenerateClause(self):
        for i, content in enumerate(self.contents):
            if not isinstance(content, list):
                continue

            if len(content) == 1:
                self.contents[i] = content[0]
                continue

            clause = ""
            size = len(content)
            for j, elem in enumerate(content):
                if j == 0:
                    clause += elem
                elif j == size-1:
                    clause += " and " + elem
                else:
                    clause += ", " + elem
            self.contents[i] = clause

    def AddDescriptor(self, key, description):
        self.descriptors[key] = description
