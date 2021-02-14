# -*- coding: utf-8 -*-
__author__ = 'mikahama'
from . import noun_tool
from syntaxmaker import syntax_maker
import random

interrogatives = ["miksi", "milloin", "kuinka", "miten"]

def create_verse(noun, mood="INDV", pos_dict=None):
    random.seed()
    if pos_dict and "adjectives" in pos_dict:
        adjective = random.choice(pos_dict["adjectives"])
    else:
        adjective = noun_tool.get_an_adjective(noun)
    if adjective is None:
        return None
    phrase = syntax_maker.create_copula_phrase()
    phrase.components["subject"] = syntax_maker.create_phrase("NP", noun, {u"PERS": "3", u"NUM": "SG"})
    np = syntax_maker.create_phrase("NP", None, {u"PERS": "3", u"NUM": "SG"})
    phrase.components["predicative"] = np
    np.components["attribute"] = syntax_maker.create_phrase("AP", adjective)
    interr =  random.choice(interrogatives)
    if interr == "kuinka" or interr == "miten":
        phrase.order = ["predicative", "head", "subject"]

    syntax_maker.set_vp_mood_and_tense(phrase, mood)
    verse = interr + " " + phrase.to_string() + "?"
    return {"verse": verse, "noun": noun, "adjective": adjective}

"""
print create_verse("mies")
print create_verse("mies")
print create_verse("mies")
print create_verse("aamu")
print create_verse("valo")
print create_verse("kone")
print create_verse("tuli")
print create_verse("kissa")
print create_verse("liekki")
print create_verse("koira")
print create_verse("isku")
print create_verse("naama")
print create_verse("peili")
print create_verse("elämä")
print create_verse("aine")
"""