from enum import Enum,IntEnum

class eDecisionVectorIndex(IntEnum):
    eDV_Assertion = 0      # Yes or no
    eDV_Confidence = 1     # The confidence of yes or no
    eDV_Verb_Strength = 2  # Magnitude of verb
    eDV_Seriousness = 3    # Seriousness of the sentence
    eDV_Tense = 4          # tense of the sentence
    eDecisionVectorSize = 5


class eNLGTense(IntEnum):
    eNLGTense_Present = 0,
    eNLGTense_Future = 1,
    eNLGTense_Past = 2


class Decision_Vector(object):
    def __init__(self):
        self.vector = [1.0] * int(eDecisionVectorIndex.eDecisionVectorSize)
    def set_assertion(self, assertion : float):
        self.vector[eDecisionVectorIndex.eDV_Assertion] = assertion
    def get_assertion(self) -> float: 
        return self.vector[eDecisionVectorIndex.eDV_Assertion]
    def set_confidence(self, confidence : float ):
        self.vector[eDecisionVectorIndex.eDV_Confidence] = confidence
    def get_confidence(self) -> float:
        return self.vector[eDecisionVectorIndex.eDV_Confidence]
    def set_verbal_strength(self, strength : float):
        self.vector[eDecisionVectorIndex.eDV_Verb_Strength] = strength
    def get_verbal_strength(self):
        return self.vector[eDecisionVectorIndex.eDV_Verb_Strenth]
    def set_seriousness(self, value : float):
        self.vector[eDecisionVectorIndex.eDV_Seriousness] = value
    def get_seriousness(self, value : float):
        return self.vector[eDecisionVectorIndex.eDV_Seriousness]
    def set_tense(self, value : int):
        self.vector[eDecisionVectorIndex.eDV_Tense] = value
    def get_tense(self, value) -> eNLGTense:
        return self.vector[eDecisionVectorIndex.eDV_Tense]