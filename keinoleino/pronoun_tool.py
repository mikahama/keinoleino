# -*- coding: utf-8 -*-
__author__ = 'mikahama'
import pickle
import random
import os
from mikatools import *

verbs = {}

pronouns = {"SG1" : "minä", "SG2" : "sinä", "SG3" : "se", "PL1" : "me", "PL2": "te", "PL3": "ne"}


def load_data():
    global verbs
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/Me_U_verbs.json")
    verbs = json_load(path)

load_data()

def list_verbs(person):
    if person in verbs:
        return verbs[person]
    else:
        return None

def give_a_verb(person):
    return WeightedPick(list_verbs(person))

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
        return ""

def pronoun(person):
    if person in pronouns:
        return pronouns[person]
    else:
        return None

def is_personal_pronoun(p_pronoun):
    if p_pronoun in pronouns.values():
        return True
    else:
        return False