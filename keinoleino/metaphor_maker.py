# -*- coding: utf-8 -*-
__author__ = 'mikahama'
from . import noun_tool
from . import verb_valence
import random
from syntaxmaker import syntax_maker



def list_possible_metaphors(word):
    metaphors = {}
    verbs = noun_tool.verbs_for_noun(word)
    threshold = threshold_for_verbs(verbs)
    for verb in verbs:
        if verbs[verb] > threshold:
            #Frequent enough!
            nouns = noun_tool.nouns_for_verb(verb)
            if len(nouns) < 1000:
                for noun in nouns:
                    if nouns[noun] > 20 and noun != word:
                        if noun in metaphors:
                            metaphors[noun].append(verb)
                        else:
                            metaphors[noun] = [verb]
    real_metaphors = {}
    for key in metaphors:
        #let's remove words that are too similar such as man and woman
        if len(metaphors[key]) < 6:
            real_metaphors[key] = metaphors[key]
    return real_metaphors

def construct_a_metaphor(noun, use_pronoun=False, pos_dict=None):
    random.seed()
    possibilities = list_possible_metaphors(noun)
    if len(possibilities) == 0:
        return None
    comp_noun = random.choice(list(possibilities.keys()))
    verb = random.choice(possibilities[comp_noun])
    metaphor_phrase = syntax_maker.create_copula_phrase()

    if use_pronoun:
        sp = syntax_maker.create_personal_pronoun_phrase("2", "SG")
        person = "2"
        number = "SG"
    else:
        sp = syntax_maker.create_phrase("NP", noun, {u"PERS": "3", u"NUM": "SG"})
        person = "3"
        number = "SG"

    metaphor_phrase.components["subject"] = sp
    metaphor_phrase.components["predicative"] = syntax_maker.create_phrase("NP", comp_noun, {u"PERS": "3", u"NUM": "SG"})
    meta_string = metaphor_phrase.to_string()
    explain_phrase = syntax_maker.create_verb_pharse(verb)
    explain_phrase.components["subject"]  = syntax_maker.create_personal_pronoun_phrase(person,number,True)

    add_adverb = True

    if "dir_object" in explain_phrase.components:
        if pos_dict:
            add_adverb = True
            dir_o = random.choice(pos_dict["nouns"])
        else:
            add_adverb = False
            dir_o = noun_tool.get_an_object(verb, "dir")
        explain_phrase.components["dir_object"] = syntax_maker.create_phrase("NP", dir_o, {u"PERS": "3", u"NUM": "SG"})
    if "indir_object" in explain_phrase.components:
        if pos_dict:
            indir_o = random.choice(pos_dict["nouns"])
        else:
            indir_o = noun_tool.get_an_object(verb, "indir")
        explain_phrase.components["indir_object"] = syntax_maker.create_phrase("NP", indir_o, {u"PERS": "3", u"NUM": "SG"})
    explain_string = explain_phrase.to_string()

    adverb = ""
    if pos_dict and "adverbs" in pos_dict:
        adverb = " " + random.choice(pos_dict["adverbs"])
    elif add_adverb:
        pos_adverb = verb_valence.get_an_adverb(verb)
        if pos_adverb is not None:
            adverb = " " + pos_adverb

    verse =  meta_string + "\n" + explain_string + adverb
    return {"verse": verse, "noun": comp_noun, "verb" : verb}


def create_a_tautology(noun, adjective=False, mood="INDV", pos_dict=None):
    random.seed()
    if pos_dict and "adjectives" in pos_dict:
        adj = random.choice(pos_dict["adjectives"])
    else:
        adj = noun_tool.get_an_adjective(noun)
    phrase = syntax_maker.create_copula_phrase("Par")
    sp = syntax_maker.create_phrase("NP", noun, {u"PERS": "3", u"NUM": "PL"})

    phrase.components["subject"] = sp
    pp = syntax_maker.create_phrase("NP", noun, {u"PERS": "3", u"NUM": "PL"})

    phrase.components["predicative"] = pp

    return_verse = {"noun": noun}
    if adjective:
        sp.components["attribute"] = syntax_maker.create_phrase("AP", adj)
        pp.components["attribute"] = syntax_maker.create_phrase("AP", adj)
        return_verse["adjective"] = adj

    syntax_maker.set_vp_mood_and_tense(phrase, mood)
    return_verse["verse"] = phrase.to_string()
    return return_verse

def threshold_for_verbs(verbs):
    frequencies = verbs.values()
    test_set = set(range(20))
    count = len(set(frequencies) - test_set)
    if count > 10:
        return 20
    else:
        return 2

"""
print create_a_tautology("kahvi")["verse"]
print create_a_tautology("ovi")["verse"]
print create_a_tautology("kaveri")["verse"]
print create_a_tautology("vesi")["verse"]
print create_a_tautology("mies")["verse"]
"""
