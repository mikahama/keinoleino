__author__ = 'mikahama'

from . import word_lookup
import random
from . import noun_tool
from syntaxmaker import syntax_maker
from . import verb_valence

def create_verse(noun, pos_dict=None):
    random.seed()
    if pos_dict:
        word = random.choice(pos_dict["nouns"])
    else:
        syns = word_lookup.get_related_words(noun)
        if len(syns) ==0:
            return None
        word = random.choice(syns)
    if word is None:
        word = noun
    verbs = noun_tool.verbs_for_noun(word)
    if len(verbs) == 0:
        verbs = noun_tool.verbs_for_noun(noun)
        if len(verbs) == 0 and pos_dict and "verbs" in pos_dict:
            verbs = pos_dict["verbs"]
        elif len(verbs) ==0:
            return None
    if "olla" in verbs:
        del verbs["olla"]
    if type(verbs) == dict:
        verb = random.choice(list(verbs.keys()))
    else:
        verb = random.choice(verbs)
    phrase = syntax_maker.create_verb_pharse(verb)

    #Start of the sentence, "aurinkona, valona..."
    phrase.order.insert(0, "Advl")
    advl = {u"CASE": "Ess" }
    phrase.governance["Advl"] = advl
    phrase.components["Advl"] = syntax_maker.create_phrase("NP",word,{u"PERS": "3", u"NUM": "SG"})


    phrase.components["subject"] = syntax_maker.create_phrase("NP","se",{u"PERS": "3", u"NUM": "SG"})
    add_adverb = True

    if "dir_object" in phrase.components:
        add_adverb = False
        if pos_dict and "nouns" in pos_dict:
            dir_o = random.choice(pos_dict["nouns"])
        else:
            dir_o = noun_tool.get_an_object(verb, "dir")
        phrase.components["dir_object"] = syntax_maker.create_phrase("NP", dir_o, {u"PERS": "3", u"NUM": "SG"})
    if "indir_object" in phrase.components:
        if pos_dict and "nouns" in pos_dict:
            indir_o = random.choice(pos_dict["nouns"])
        else:
            indir_o = noun_tool.get_an_object(verb, "indir")
        phrase.components["indir_object"] = syntax_maker.create_phrase("NP", indir_o, {u"PERS": "3", u"NUM": "SG"})
    explain_string = phrase.to_string()

    adverb = ""
    if pos_dict and "adverbs" in pos_dict:
        adverb = " " + random.choice(pos_dict["adverbs"])
    if add_adverb:
        pos_adverb = verb_valence.get_an_adverb(verb)
        if pos_adverb is not None:
            adverb = pos_adverb + " "

    verse = adverb + explain_string
    return {"verse": verse, "noun": word, "verb": verb}


"""
print create_verse("aurinko")
print create_verse("valo")
print create_verse("ilo")
print create_verse("kettu")
print create_verse("kissa")
print create_verse("mies")
print create_verse("katu")
"""