import os
from nltk.corpus import wordnet as wn

"""

    !Check the wiki page for documentation!

"""
unicode = str

def get_lemma(word):
	if type(word) is unicode:
		word = word.encode('utf-8')

	result = os.popen("echo \"" + word + "\" | omorfi-analyse-text.sh").read()
	correct_line = False
	for line in result.splitlines():
		if correct_line:
			results = line.split("\t")
			try:
				results = results[1].split(" ")
				return results[0]
			except:
				return ""
		if line.startswith(word):
			correct_line = True
	return ""


def get_related_words(o_lemma):
	related_words = []
	synsets = wn.synsets(o_lemma, lang="fin")
	for synset in synsets:
		lemmas = synset.lemma_names('fin')
		if lemmas is not None:
			for lemma in lemmas:
				if lemma not in related_words and lemma != o_lemma and "_" not in lemma and not unicode(lemma).endswith("t"):
					related_words.append(lemma)
	return related_words


def get_antonyms(lemma):
	antonyms = []
	synsets = wn.synsets(lemma, lang="fin")
	for synset in synsets:
		lemmas = synset.lemmas(lang="en")
		if lemmas is not None:
			for lemma in lemmas:
				lemma_antonyms = lemma.antonyms()
				if lemma_antonyms is not None:
					for antonym in lemma_antonyms:
						try:
							lemma_name = wn.synsets(antonym.name())[0].lemma_names("fin")[0]
							antonyms.append(lemma_name.replace("_", " "))
						except:
							# No translation in Finnish
							pass
	return antonyms


def get_hypo_and_hyper(lemma):
	hyps = []
	synsets = wn.synsets(lemma, lang="fin")
	if len(synsets) > 0:
		hyp_syns = synsets[0].hypernyms() + synsets[0].hyponyms()
		for hyp_syn in hyp_syns:
			lemmas = hyp_syn.lemma_names("fin")
			if lemmas is not None and len(lemmas) > 0:
				for lem in lemmas:
					if "_" not in lem:
						hyps.append(lem)
	return hyps



def get_robot_words(lemma):
	if type(lemma) is str:
		lemma = lemma.decode('utf-8')

	words = get_related_words(lemma)
	antonyms = get_antonyms(lemma)
	hypos = get_hypo_and_hyper(lemma)

	result = set(words + antonyms + hypos)
	if len(result) == 0:
		result = []

	return result


