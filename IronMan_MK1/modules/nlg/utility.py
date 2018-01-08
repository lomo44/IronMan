import json

def to_past_tense(verb : str):
    if verb in modal_verb_list:
        return verb
    elif verb in irregular_past:
        return irregular_past[verb]
    elif verb[-1] == 'e':
        return verb + 'd'
    elif verb[-1] == 'y':
        return verb[0:-1] + "ied"
    elif verb[-1] == 'c':
        return verb[0:-1] + "ked"
    elif verb[-1] in double_ending_list and verb[-2] in vowel_list:
        return verb + verb[-1]+ "ed"
    else:
        return verb + 'ed'

def to_past_participle(verb : str):
    if verb in modal_verb_list:
        return verb
    elif verb in irregular_past:
        return irregular_past_participle[verb]
    elif verb[-1] == 'e':
        return verb + 'd'
    elif verb[-1] == 'y':
        return verb[0:-1] + "ied"
    elif verb[-1] == 'c':
        return verb[0:-1] + "ked"
    elif verb[-1] in double_ending_list and verb[-2] in vowel_list:
        return verb + verb[-1] + "ed"
    else:
        return verb + 'ed'

def to_progressive(verb : str):
    if verb in modal_verb_list:
        return verb
    elif verb[-2:] == 'ee':
        return verb + 'ing'
    elif verb[-2:] == 'ie':
        return verb[0:-2] + 'ying'
    elif verb[-1] == 'e':
        return verb[0:-1] + "ing"
    elif verb[-1] in double_ending_list and verb[-2] in vowel_list:
        return verb + verb[-1] + "ing"
    else:
        return verb + 'ing'

modal_verb_list = ["can", "could", "may", "might", "will", "would", "shall", "should", "must"]

irregular_past = {
    "arise": "arose",
    "babysit": "babysat",
    "is": "was",
    "are": "were",
    "beat": "beat",
    "become": "became",
    "bend": "bent",
    "begin": "began",
    "bet": "bet",
    "bind": "bound",
    "bite": "bit",
    "bleed": "bled",
    "blow": "blew",
    "break": "broke",
    "breed": "bred",
    "bring": "brought",
    "broadcast": "broadcast",
    "build": "built",
    "buy": "bought",
    "catch": "caught",
    "choose": "chose",
    "come": "came",
    "cost": "cost",
    "cut": "cut",
    "deal": "dealt",
    "dig": "dug",
    "do": "did",
    "draw": "drew",
    "drink": "drank",
    "drive": "drove",
    "eat": "ate",
    "fall": "fell",
    "feed": "fed",
    "feel": "felt",
    "fight": "fought",
    "find": "found",
    "fly": "flew",
    "forbid": "forbade",
    "forget": "forgot",
    "forgive": "forgave",
    "freeze": "froze",
    "get": "got",
    "give": "gave",
    "go": "went",
    "grow": "grew",
    "hang": "hung",
    "have": "had",
    "hear": "heard",
    "hide": "hid",
    "hit": "hit",
    "hold": "held",
    "hurt": "hurt",
    "keep": "kept",
    "know": "knew",
    "lay": "laid",
    "lead": "led",
    "leave": "left",
    "lend": "lent",
    "let": "let",
    "lie": "lay",
    "light": "lit",
    "lose": "lost",
    "make": "made",
    "mean": "meant",
    "meet": "met",
    "pay": "paid",
    "put": "put",
    "quit": "quit",
    "read": "read",
    "ride": "rode",
    "ring": "rang",
    "rise": "rose",
    "run": "ran",
    "say": "said",
    "see": "saw",
    "sell": "sold",
    "send": "sent",
    "set": "set",
    "shake": "shook",
    "shine": "shone",
    "shoot": "shot",
    "show": "showed",
    "shut": "shut",
    "sing": "sang",
    "sink": "sank",
    "sit": "sat",
    "sleep": "slept",
    "slide": "slid",
    "speak": "spoke",
    "spend": "spent",
    "spin": "spun",
    "spread": "spread",
    "stand": "stood",
    "steal": "stole",
    "stick": "stuck",
    "sting": "stung",
    "strike": "struck",
    "swear": "swore",
    "sweep": "swept",
    "swim": "swam",
    "swing": "swung",
    "take": "took",
    "teach": "taught",
    "tear": "tore",
    "tell": "told",
    "think": "thought",
    "throw": "threw",
    "understand": "understood",
    "wake": "woke",
    "wear": "wore",
    "win": "won",
    "withdraw": "withdrew",
    "write": "wrote"
}
irregular_past_participle = {
    "arise": "arisen",
    "babysit": "babysat",
    "is": "been",
    "are": "been",
    "beat": "beaten",
    "become": "become",
    "bend": "bent",
    "begin": "begun",
    "bet": "bet",
    "bind": "bound",
    "bite": "bitten",
    "bleed": "bled",
    "blow": "blown",
    "break": "broken",
    "breed": "bred",
    "bring": "brought",
    "broadcast": "broadcast",
    "build": "built",
    "buy": "bought",
    "catch": "caught",
    "choose": "chosen",
    "come": "come",
    "cost": "cost",
    "cut": "cut",
    "deal": "dealt",
    "dig": "dug",
    "do": "done",
    "draw": "drawn",
    "drink": "drunk",
    "drive": "driven",
    "eat": "eaten",
    "fall": "fallen",
    "feed": "fed",
    "feel": "felt",
    "fight": "fought",
    "find": "found",
    "fly": "flown",
    "forbid": "forbidden",
    "forget": "forgotten",
    "forgive": "forgiven",
    "freeze": "frozen",
    "get": "gotten",
    "give": "given",
    "go": "gone",
    "grow": "grown",
    "hang": "hung",
    "have": "had",
    "hear": "heard",
    "hide": "hidden",
    "hit": "hit",
    "hold": "held",
    "hurt": "hurt",
    "keep": "kept",
    "know": "known",
    "lay": "laid",
    "lead": "led",
    "leave": "left",
    "lend": "lent",
    "let": "let",
    "lie": "lain",
    "light": "lit",
    "lose": "lost",
    "make": "made",
    "mean": "meant",
    "meet": "met",
    "pay": "paid",
    "put": "put",
    "quit": "quit",
    "read": "read",
    "ride": "ridden",
    "ring": "rung",
    "rise": "risen",
    "run": "run",
    "say": "said",
    "see": "seen",
    "sell": "sold",
    "send": "sent",
    "set": "set",
    "shake": "shaken",
    "shine": "shone",
    "shoot": "shot",
    "show": "shown",
    "shut": "shut",
    "sing": "sung",
    "sink": "sunk",
    "sit": "sat",
    "sleep": "slept",
    "slide": "slid",
    "speak": "spoken",
    "spend": "spent",
    "spin": "spun",
    "spread": "spread",
    "stand": "stood",
    "steal": "stolen",
    "stick": "stuck",
    "sting": "stung",
    "strike": "struck",
    "swear": "sworn",
    "sweep": "swept",
    "swim": "swum",
    "swing": "swung",
    "take": "taken",
    "teach": "taught",
    "tear": "torn",
    "tell": "told",
    "think": "thought",
    "throw": "thrown",
    "understand": "understood",
    "wake": "woken",
    "wear": "worn",
    "win": "won",
    "withdraw": "withdrawn",
    "write": "written"
}

vowel_list = ["a", "e", "i", "o", "u"]
double_ending_list = [ "b", "d", "g", "l", "m", "n", "p", "r", "t"]

if __name__ == "__main__":
    test_verbs = ["do","die","stop","climb","see"]
    for verb in test_verbs:
        print(to_past_tense(verb),to_past_participle(verb),to_progressive(verb))
