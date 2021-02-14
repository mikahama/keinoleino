# -*- coding: utf-8 -*-
__author__ = 'mikahama'
from . import word_lookup
from . import noun_tool
import random
from syntaxmaker import syntax_maker


def paraphrase(noun, pos_dict=None):
    random.seed()
    hyps = word_lookup.get_hypo_and_hyper(noun)
    if pos_dict and "nouns" in pos_dict:
        hyps = pos_dict["nouns"]
    if len(hyps) ==0:
        return None
    hyp = random.choice(hyps)
    if pos_dict and "adjectives" in pos_dict:
        adj = random.choice(pos_dict["adjectives"])
    else:
        adj = noun_tool.get_an_adjective(noun)
    np = syntax_maker.create_phrase("NP", hyp, {u"PERS": "3", u"NUM": "SG"})
    np.components["attribute"] = syntax_maker.create_phrase("AP", adj)
    return np

def add_adjective(noun, pos_dict=None):
    random.seed()
    if pos_dict and "adjectives" in pos_dict:
        adj = random.choice(pos_dict["adjectives"])
    else:
        adj = noun_tool.get_an_adjective(noun)
    np = syntax_maker.create_phrase("NP", noun, {u"PERS": "3", u"NUM": "PL"})
    np.components["attribute"] = syntax_maker.create_phrase("AP", adj)
    return np

def create_paraphrase(noun, pos_dict=None):
    random.seed()
    pp = paraphrase(noun)
    if pp is None:
        return None

    pp.morphology[u"CASE"] = "Nom"
    verse = noun + ", tuo " + pp.to_string()
    return {"verse": verse, "noun": pp.head.lemma}


def address_interlocutor(noun, pos_dict=None):
    return {"verse" :  noun + ", ", "noun":noun}

def relative_verse(noun, pos_dict=None):
    random.seed()
    main_np = syntax_maker.create_personal_pronoun_phrase("3", "SG")
    if pos_dict and "nouns" in pos_dict:
        rel_ws = pos_dict["nouns"]
    else:
        rel_ws = word_lookup.get_related_words(noun)
    if len(rel_ws) == 0:
        synonym = noun
    else:
        synonym = random.choice(rel_ws)
    if pos_dict and "verbs" in pos_dict:
        random.seed()
        verb1 = random.choice(pos_dict["verbs"])
        verb2 = random.choice(pos_dict["verbs"])
    else:
        verb1 = noun_tool.get_a_verb(synonym)
        verb2 = noun_tool.get_a_verb(noun)
    if verb1 is None:
        verb1 = noun_tool.get_a_verb(noun)
    if verb1 is None or verb2 is None:
        return None
    relative_p = syntax_maker.create_verb_pharse(verb1)
    relative_p.components["dir_object"] = syntax_maker.create_phrase("NP", synonym)
    syntax_maker.add_relative_clause_to_np(main_np, relative_p, subject=True)
    phrase = syntax_maker.create_verb_pharse(verb2)
    phrase.components["subject"] = main_np
    phrase.components["dir_object"] = syntax_maker.create_phrase("NP", noun)

    return {"verse": str(phrase), "noun":noun}

"""
print relative_verse("mies")
print relative_verse("kissa")
print relative_verse("koira")
print relative_verse("talo")
print relative_verse("linna")
"""
