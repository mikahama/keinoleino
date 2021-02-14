# -*- coding: utf-8 -*-
__author__ = 'mikahama'
import pickle
import random
from .fake_djangodb import nouns, nouns_filter
from .fake_djangodb import verbs
import json

adjectives = None

stop_adjs = ["lainen", "samainen", "oma", "kaltainen", "tuntuinen", "näköinen", "mukainen","suuntainen", "värinen", "niminen"]

CCs = [ "ja", "sekä", "eli", "tai","vai", "mutta", "vaan", "sillä"]
CSs = [ "että", "jotta", "koska", "kun", "jos", "vaikka", "kuin", "kunnes"]

def get_a_conjunction(type="CC"):
    random.seed()
    if type == "CC":
        return random.choice(CCs)
    else:
        return random.choice(CSs)

def is_abstract(word):
    return False


def verbs_for_noun(noun):
    try:
        global nouns
        nouns_text = nouns(word=noun).verbs
        ns = json.loads(nouns_text)
        return ns
    except:
        return {}

def nouns_for_verb(verb):
    try:
        nouns_text = verbs(word=verb).subjects
        nos = json.loads(nouns_text)
        return nos
    except:
        return {}

def get_nouns_for_random_noun():
    random.seed()
    global nouns
    ns = nouns_filter()
    return_dict = {}
    while len(return_dict.keys()) < 6:
        noun = random.choice(ns)
        nos = json.loads(noun.nouns)
        if len(nos.keys()) != 0:
            return_dict.update(nos)
    return return_dict

def nouns_for_nouns(noun):
    try:
        global nouns
        nouns_text = nouns(word=noun).nouns
        ns = json.loads(nouns_text)
        return ns
    except:
        return {}

def objects_for_verb(verb):
    try:
        nouns_text = verbs(word=verb).objs
        nous = json.loads(nouns_text)
        return nous
    except:
        return {"dir":{}, "indir": {}}

def WeightedPick(d):
    k = None
    r = random.uniform(0, sum(d.values()))
    s = 0.0
    for k, w in d.items():
        s += w
        if r < s: return k
    if k is not None:
        return k
    else:
        return None

def get_a_verb(noun):
    objs = verbs_for_noun(noun)
    if "olla" in objs:
        del objs["olla"]
    return WeightedPick(objs)

def get_an_object(verb, obj_type):
    objs = objects_for_verb(verb)
    objs = objs[obj_type]
    return WeightedPick(objs)

def adjectives_for_noun(noun):
    try:
        global nouns
        nouns_text = nouns(word=noun).adjectives
        adjs = json.loads(nouns_text)
        for adj in stop_adjs:
            if adj in adjs:
                del adjs[adj]
        if adjs is None:
            return {}
        else:
            return adjs
    except:
        return {}

def get_an_adjective(noun):
    adj =  WeightedPick(adjectives_for_noun(noun))
    if adj is not None:
        adj = adj.replace("|", "")
    else:
        #No adjective -> give at least an adjective
        adj = get_random_adjective()
    return adj

def get_random_adjective():
    random.seed()
    global nouns
    adjectives = nouns_filter(has_adjectives = True)
    noun = random.choice(adjectives)
    adj = random.choice(list(json.loads(noun.adjectives).keys()))
    return adj

def get_random_noun():
    random.seed()
    global nouns
    ns = nouns_filter()
    noun = random.choice(ns)
    return noun

def get_random_adjectives():
    random.seed()
    global nouns
    adjectives = nouns_filter(has_adjectives = True)
    return_dict = {}
    while len(return_dict.keys()) < 6:
        noun = random.choice(adjectives)
        adjs = json.loads(noun.adjectives)
        if len(adjs.keys()) != 0:
            return_dict.update(adjs)
    return return_dict

def get_random_nouns(syntactic_position = "subj"):
    random.seed()
    global nouns
    all_nouns = nouns_filter(has_adjectives = True)
    count = len(all_nouns)
    slice = random.random() * (count - 10)
    ns = all_nouns[slice: slice+10]
    results = []
    for n in ns:
        results.append(n.word)
    return results

