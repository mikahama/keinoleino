# -*- coding: utf-8 -*-
__author__ = 'mikahama'
from . import noun_tool
from syntaxmaker import syntax_maker
from . import pronoun_tool
from . import verb_valence
import random

attitude_verbs = ["kuvitella", "toivoa", "haluta", "ajatella", "nähdä", "kuulla", "epäillä", "uskoa", "tuntea", "tietää"]
attitude_conjunctions = ["että", "ennen kuin", "vaikka", "kun"]
counterfactual_conjunctions = ["jos", "vaikka", "mikäli"]


def create_verse(noun, person="SG1", pos_dict = None):
    random.seed()
    opinion = subjective_opinion(noun, person, pos_dict)
    adj = adjective_description(noun, person, pos_dict)
    verses = ""
    return_vals = {"noun": noun}
    if opinion is not None:
        verses = opinion["verse"]
        return_vals["verb"] = opinion["verb"]
    if adj is not None:
        return_vals["adjective"] = adj["adjective"]
        if verses == "":
            verses = adj["verse"]
        else:
            verses = verses + "\n" + adj["verse"]

    return_vals["verse"] = verses
    return return_vals

def subjective_opinion(noun, person="SG1", aux=None, pos_dict = None):
    random.seed()
    if pos_dict and "verbs" in pos_dict:
        verb = random.choice(pos_dict["verbs"])
    else:
        while True:
            verb = pronoun_tool.give_a_verb(person)
            if verb is None:
                return None
            if verb_valence.is_copula(verb) or syntax_maker.is_auxiliary_verb(verb):
                pass
            elif verb_valence.valency_count(verb) > 1:
                break
    phrase = syntax_maker.create_verb_pharse(verb)

    num = person[:2]
    pers = person[2:]

    phrase.components["subject"] = syntax_maker.create_phrase("NP", pronoun_tool.pronoun(person), {u"PERS": pers, u"NUM": num})

    if "indir_object" in phrase.components:
        indir_o = noun
        if pos_dict and "nouns" in pos_dict:
            dir_o = random.choice(pos_dict["nouns"])
        else:
            dir_o = noun_tool.get_an_object(verb, "dir")
    else:
        dir_o = noun


    if "dir_object" in phrase.components:
        phrase.components["dir_object"] = syntax_maker.create_phrase("NP", dir_o, {u"PERS": "3", u"NUM": "SG"})
    if "indir_object" in phrase.components:
        phrase.components["indir_object"] = syntax_maker.create_phrase("NP", indir_o, {u"PERS": "3", u"NUM": "SG"})

    if aux is None:
        aux = random.choice([True, False])
    if aux:
        syntax_maker.add_auxiliary_verb_to_vp(phrase)

    if random.choice([True, False]):
        syntax_maker.negate_verb_pharse(phrase)
    return {"verse": phrase.to_string(), "noun": dir_o, "verb": verb}


def adjective_description(noun, person="SG1", question=None, pos_dict=None):
    random.seed()
    if pos_dict and "adjectives" in pos_dict:
        adjective = random.choice(pos_dict["adjectives"])
    else:
        adjective = noun_tool.get_an_adjective(noun)
    if adjective is None:
        return None

    phrase = syntax_maker.create_copula_phrase()
    num = person[:2]
    pers = person[2:]
    phrase.components["subject"] = syntax_maker.create_phrase("NP", None, {u"PERS": pers, u"NUM": num})
    np = syntax_maker.create_phrase("NP", None, {u"PERS": "3", u"NUM": num})
    phrase.components["predicative"] = np
    np.components["attribute"] = syntax_maker.create_phrase("AP", adjective)

    interrog = ""
    if question is None:
        question = random.choice([True, False])
    if question:
        syntax_maker.turn_vp_into_question(phrase)
        interrog = "?"

    return {"verse": phrase.to_string()+interrog, "noun": noun, "adjective": adjective}


def propositional_attitude(noun, person="SG1", question=None, negation=None, prodrop=False, pos_dict=None):
    random.seed()

    #Main clause
    attitude_subject = None
    if not prodrop:
        attitude_subject = pronoun_tool.pronoun(person)
    num = person[:2]
    pers = person[2:]
    attitude_verb = random.choice(attitude_verbs)
    attitude_phrase = syntax_maker.create_verb_pharse(attitude_verb)
    attitude_phrase.components["subject"] = syntax_maker.create_phrase("NP", attitude_subject, {u"PERS": pers, u"NUM": num})
    interrog = ""

    if negation is None:
        negation = random.choice([True, False])
    if negation:
        syntax_maker.negate_verb_pharse(attitude_phrase)

    if question is None:
        question = random.choice([True, False])
    if question:
        syntax_maker.turn_vp_into_question(attitude_phrase)
        interrog = "?"

    #Subordinate clause

    verb = noun_tool.get_a_verb(noun)
    if verb is None:
        return None

    vp = syntax_maker.create_verb_pharse(verb)
    vp.components["subject"] = syntax_maker.create_phrase("NP", noun, {u"PERS": "3", u"NUM": "SG"})
    add_adverb = True
    if "dir_object" in vp.components:
        add_adverb = False
        if pos_dict and "nouns" in pos_dict:
            dir_o = random.choice(pos_dict["nouns"])
        else:
            dir_o = noun_tool.get_an_object(verb, "dir")
        noun = dir_o
        vp.components["dir_object"] = syntax_maker.create_phrase("NP", dir_o, {u"PERS": "3", u"NUM": "SG"})
    if "indir_object" in vp.components:
        if pos_dict and "nouns" in pos_dict:
            indir_o = random.choice(pos_dict["nouns"])
        else:
            indir_o = noun_tool.get_an_object(verb, "indir")
        vp.components["indir_object"] = syntax_maker.create_phrase("NP", indir_o, {u"PERS": "3", u"NUM": "SG"})

    adverb = ""
    if add_adverb:
        if pos_dict and "adverbs" in pos_dict:
            pos_adverb = random.choice(pos_dict["adverbs"])
        else:
            pos_adverb = verb_valence.get_an_adverb(verb)
        if pos_adverb is not None:
            adverb = " " + pos_adverb

    conjunction = random.choice(attitude_conjunctions)
    verse = attitude_phrase.to_string() + ", " + conjunction + " " + vp.to_string() + adverb +interrog
    return {"verse": verse, "noun": noun, "verb": verb}


def counterfactual_verse(noun, person="SG1", question=None, negation=None, prodrop=False, use_pronoun=False, passive=False, pos_dict=None):
    random.seed()
    num = person[:2]
    pers = person[2:]

    subject = None
    if not prodrop:
        subject = pronoun_tool.pronoun(person)

    interrog = ""
    if pos_dict and "verbs" in pos_dict:
        verb = random.choice(pos_dict["verbs"])
    else:
        verb = noun_tool.get_a_verb(noun)
    if verb is None:
        return None
    condition_phrase = syntax_maker.create_verb_pharse(verb)
    condition_phrase.morphology[u"MOOD"] = "COND"
    if use_pronoun:
        p_num = num
        if pers == "1":
            p_pers = "2"
        else:
            p_pers = "1"
        sp = syntax_maker.create_personal_pronoun_phrase(p_pers,p_num)
    else:
        sp =syntax_maker.create_phrase("NP",noun, {u"PERS": "3", u"NUM": "PL"})
    condition_phrase.components["subject"] = sp
    dir_o = None
    if "dir_object" in condition_phrase.components:
        if pos_dict and "nouns" in pos_dict:
            dir_o = random.choice(pos_dict["nouns"])
        else:
            dir_o = noun_tool.get_an_object(verb, "dir")
        condition_phrase.components["dir_object"] = syntax_maker.create_phrase("NP", dir_o, {u"PERS": "3", u"NUM": "SG"})
    if "indir_object" in condition_phrase.components:
        if pos_dict and "nouns" in pos_dict:
            indir_o = random.choice(pos_dict["nouns"])
        else:
            indir_o = noun_tool.get_an_object(verb, "indir")
        condition_phrase.components["indir_object"] = syntax_maker.create_phrase("NP", indir_o, {u"PERS": "3", u"NUM": "SG"})

    if negation is None:
        negation = random.choice([True, False])
    if negation:
        syntax_maker.negate_verb_pharse(condition_phrase)

    if passive:
        syntax_maker.turn_vp_to_passive(condition_phrase)

    if pos_dict and "verbs" in pos_dict:
        verb = random.choice(pos_dict["verbs"])
    else:
        while True:
            verb = pronoun_tool.give_a_verb(person)
            if verb is None:
                return None
            if verb_valence.is_copula(verb) or syntax_maker.is_auxiliary_verb(verb):
                pass
            elif verb_valence.valency_count(verb) > 1:
                break
    phrase = syntax_maker.create_verb_pharse(verb)
    phrase.morphology[u"MOOD"] = "COND"

    phrase.components["subject"] = syntax_maker.create_phrase("NP", subject, {u"PERS": pers, u"NUM": num})
    if "dir_object" in phrase.components:
        if use_pronoun:
            dop = syntax_maker.create_personal_pronoun_phrase(p_pers,p_num)
        else:
            dop = syntax_maker.create_phrase("NP", noun, {u"PERS": "3", u"NUM": "SG"})
        phrase.components["dir_object"] = dop
    if "indir_object" in phrase.components:
        if pos_dict and "nouns" in pos_dict:
            indir_o = random.choice(pos_dict["nouns"])
        else:
            indir_o = noun_tool.get_an_object(verb, "indir")
        phrase.components["indir_object"] = syntax_maker.create_phrase("NP", indir_o, {u"PERS": "3", u"NUM": "SG"})


    if question is None:
        question = random.choice([True, False])
    if question:
        syntax_maker.turn_vp_into_question(phrase)
        interrog = "?"

    return_verse = {"noun":noun, "verb": verb}
    if dir_o is not None:
        return_verse["noun"] = dir_o
    conjunction = random.choice(counterfactual_conjunctions)
    return_verse["verse"] = conjunction + " " + condition_phrase.to_string() + ", " + phrase.to_string() + interrog
    return return_verse

"""
print counterfactual_verse("auto" , "SG2")["verse"]
print counterfactual_verse("mies" , "SG2")["verse"]
print counterfactual_verse("talo" , "SG1")["verse"]
print counterfactual_verse("koira" , "SG1")["verse"]
print counterfactual_verse("mies" , "SG1")["verse"]
print counterfactual_verse("aamu" , "SG1")["verse"]
print counterfactual_verse("suru" , "SG2")["verse"]
print counterfactual_verse("aurinko" , "SG2")["verse"]
print counterfactual_verse("valo" , "SG2")["verse"]
print counterfactual_verse("ilo" , "SG2")["verse"]
print counterfactual_verse("kissa" , "SG2")["verse"]
"""
