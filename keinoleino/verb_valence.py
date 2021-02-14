# -*- coding: utf-8 -*-
import pickle
import os
import random
from .fake_djangodb import verbs, verbs_filter
import json
from mikatools import *

valences = {}
direct_cases = {"Gen", "Par", "Ela", "Ill"}
indirect_cases = {"Ess", "Tra", "Abl", "All", "Ill"}
direct_threshold = 0.23
indirect_threshold = 0.18

adverbs = json_load(script_path("data/adverbs_keys.json"))

stop_adverbs = ["laisesti", "näköisesti", "kuuloisesti", "kaltaisesti"]

def load_valences_from_bin():
	"""
	Loads a dictionary dump to a global variable containing verbs together with the number of complements they can get
	"""
	global valences
	valence_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'verb_valences_new.json')
	valences = json_load(valence_path)


load_valences_from_bin()


def suitable_adverbs(verb):
	"""
	Returns a dictionary of adverbs that have appeared with the verb in the corpus. Keys are adverbs, values their frequencies with the verb
	:param verb: a verb "juosta"
	:return: a dictionary of adverbs {"hitaasti": 52, "nopeasti":85...} can be an empty dictionary {}
	"""
	try:
		advs_text = verbs(word=verb).adverbs
		advs = json.loads(advs_text)
	except:
		return {}

	for adverb in stop_adverbs:
		if adverb in advs:
			del advs[adverb]
	return advs


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


def get_an_adverb(verb):
	"""
	Returns an adverb suitable for a verb or a random one
	:param verb: a verb "juosta"
	:return: adverb "hitaasti"
	"""
	objs = suitable_adverbs(verb)
	adv=  WeightedPick(objs)
	if adv is None:
		return get_random_adverb()
	else:
		return adv


def get_random_adverb():
	"""
	Returns an adverb at random
	:return: an adverb "kiivaasti"
	"""
	advs = adverbs
	random.seed()
	adv = random.choice(advs)
	return adv

def get_random_adverbs():
	"""
	Returns a list of adverbs at random
	:return: a list of adverbs ["kiivaasti", "kovaa"...]
	"""
	vs = adverbs
	count = vs.count()
	index = random.randint(0, count - 11)
	vs = vs[index: index+10]
	return_list = []
	for item in vs:
		return_list.append(item.word)
	return return_list


def cases_total(verb, cases_list):
	global valences
	if verb not in valences:
		return 0
	cases = valences[verb]
	count = 0
	for case in cases:
		if case in cases_list:
			count = count + cases[case]
	return count

def get_random_verbs(valency_c=1, order=[]):
	"""
	Outputs random verbs that can have valency_c complements or the complements stated in the order list
	:param valency_c: a number from 1 to 3
	:param order: an optional list ["subject", "head", "dir_object"]
	:return:
	"""
	if u"dir_object" in order:
		valency_c = 2
	if u"indir_object" in order:
		valency_c = 3
	vs = verbs_filter(valency_count=valency_c)
	count = vs.count()
	index = random.randint(0, count - 11)
	vs = vs[index: index+10]
	return_list = []
	for item in vs:
		return_list.append(item.word)
	return return_list

def all_cases_total(verb):
	global indirect_cases
	global direct_cases
	return cases_total(verb, indirect_cases) + cases_total(verb, direct_cases)


def verb_objects(verb, cases_list, threshold):
	global valences
	if verb not in valences:
		return {}
	total = float(all_cases_total(verb))
	object_cases = {}
	verb_cases = valences[verb]
	for case in cases_list:
		if case in verb_cases:
			ratio = verb_cases[case] / total
			if ratio > threshold:
				object_cases[case] = ratio
	return object_cases


def verb_direct_objects(verb):
	global direct_cases
	global direct_threshold
	objs = verb_objects(verb, direct_cases, direct_threshold)
	return objs


def verb_indirect_objects(verb):
	global indirect_cases
	global indirect_threshold
	objs = verb_objects(verb, indirect_cases, indirect_threshold)
	return objs


def valency_count(verb):
	direct_objects = verb_direct_objects(verb)
	indirect_objects = verb_indirect_objects(verb)
	if not direct_objects:
		# If the verb has no direct objects, it can only have a subject
		return 1
	elif not indirect_objects:
		# The verb has a direct object but no indirect objects
		if most_frequent_case(direct_objects) == "Gen" and "Par" not in direct_objects:
			# In case of genetive, partitive cases must also be present due to the Finnish syntax
			# If no partitive cases are present, genetives obtained from bigrams may be something else than direct objects
			return 1
		else:
			return 2
	else:
		if most_frequent_case(direct_objects) == most_frequent_case(indirect_objects):
			#Direct and indirect objects would be the same, so only direct object
			return 2
		else:
			# The verb has both kinds of objects
			return 3


def most_frequent_case(case_dict):
	m_case = ""
	m_count = 0
	for case in case_dict:
		if case_dict[case] > m_count:
			m_count = case_dict[case]
			m_case = case
	return m_case


def inflect_noun(noun, case):
	case = case.upper()
	query = "[WORD_ID=" + noun + "][POS=NOUN][NUM=SG][CASE=" + case + "]"
	result = os.popen("echo \"" + query + "\" | omorfi-generate.sh").read()
	word = result.split("\t")[1]
	if "[" in word:
		# Fail
		return None
	else:
		return word


def inflect_objects(verb, direct_object, indirect_object=None):
	vals = valency_count(verb)
	if vals < 2:
		# The verb has no objects -> can't inflect
		return []
	direct_case = most_frequent_case(verb_direct_objects(verb))
	indirect_case = None
	if vals == 3:
		indirect_case = most_frequent_case(verb_indirect_objects(verb))
	direct = inflect_noun(direct_object, direct_case)
	if indirect_case is not None and indirect_object is not None:
		indirect = inflect_noun(indirect_object, indirect_case)
		return [direct, indirect]
	else:
		return [direct]


def is_copula(verb):
	if verb == "olla":
		# There's only one copulative verb in Finnish
		return True
	else:
		return False

