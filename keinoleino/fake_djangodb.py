"""
noun_tool.py
30:    nouns_text = nouns.objects.get(word=noun).verbs
38:        nouns_text = verbs.objects.get(word=verb).subjects
59:        nouns_text = nouns.objects.get(word=noun).nouns
67:        nouns_text = verbs.objects.get(word=verb).objs
99:        nouns_text = nouns.objects.get(word=noun).adjectives

verb_valence.py
35:		advs_text = verbs.objects.get(word=verb).adverbs
"""
from mikatools import *
import json
import sqlite3

class Dummy(object):
	"""docstring for Dummy"""
	def __init__(self, kwargs):
		for k, d in kwargs.items():
			setattr(self, k, d)

conn = sqlite3.connect(script_path("data/SemFi.db"))
cursor = conn.cursor()	


def nouns_filter(has_adjectives=True):
	t = (has_adjectives,)
	cursor.execute('SELECT word, verbs, adjectives, nouns, has_adjectives FROM koululaiset_nouns WHERE has_adjectives=?', t)
	ds = cursor.fetchall()
	ds_out = []
	for d in ds:
		if d is None:
			d = ["","",""]
		data = {}
		for name, json_data in zip(["word", "verbs", "adjectives", "nouns", "has_adjectives"],d):
			try:
				#if type(json_data) is bool:
				if type(json_data) is str:
					json_data =json_data.replace("Ã¤", "ä")
				data[name] = json_data
				#else:
				#	data[name] = json.loads(json_data)
			except:
				data[name] ={}
		ds_out.append(Dummy(data))
	return ds_out

def nouns(word=""):
	t = (word,)
	cursor.execute('SELECT word, verbs, adjectives, nouns, has_adjectives FROM koululaiset_nouns WHERE word=?', t)
	d = cursor.fetchone()
	if d is None:
		d = ["","",""]
	data = {}
	for name, json_data in zip(["word", "verbs", "adjectives", "nouns", "has_adjectives"],d):
		try:
			if type(json_data) is str:
				json_data =json_data.replace("Ã¤", "ä")
			data[name] = json_data
			#else:
			#	data[name] = json.loads(json_data)
		except:
			data[name] ={}
	return Dummy(data)

def verbs(word=""):
	t = (word,)
	cursor.execute('SELECT word, subjects, objs, valency_count FROM koululaiset_verbs WHERE word=?', t)
	d = cursor.fetchone()
	if d is None:
		d = ["","",""]
	data = {}
	for name, json_data in zip(["word", "subjects", "objs","valency_count"],d):
		try:
			if type(json_data) is str:
				json_data =json_data.replace("Ã¤", "ä")
			data[name] = json_data
			#else:
			#	data[name] = json.loads(json_data)
		except:
			data[name] ={}
	return Dummy(data)


def verbs_filter(valency_count=1):
	t = (valency_count,)
	cursor.execute('SELECT word, subjects, objs, valency_count FROM koululaiset_verbs WHERE valency_count=?', t)
	ds = cursor.fetchall()
	ds_all = []
	for d in ds:
		if d is None:
			d = ["","",""]
		data = {}
		for name, json_data in zip(["word", "subjects", "objs","valency_count"],d):
			try:
				if type(json_data) is str:
					json_data =json_data.replace("Ã¤", "ä")
				data[name] = json_data
				#else:
				#	data[name] = json.loads(json_data)
			except:
				data[name] ={}
		ds_all.append(Dummy(data))
	return ds_all