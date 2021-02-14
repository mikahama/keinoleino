import pickle, codecs, json, sys

def to_uni(stri):
	try:
		return stri.decode('unicode-escape')
	except:
		print(stri)
		return None

def fixu_san(something):
	if type(something) is dict:
		new_something = {}
		for key, value in something.items():
			k = to_uni(key)
			if k is None:
				continue
			new_something[k] = fixu_san(value)
		return new_something
	elif type(something) is list:
		new_list = []
		for item in something:
			it = fixu_san(item)
			if it is None:
				continue
			new_list.append(it)
		return new_list
	elif type(something) is str:
		s = to_uni(something)
		if s is None:
			s = "None"
		return s
	else:
		return something

	

pickle_file = sys.argv[1]
print(pickle_file)
data = pickle.load(open(pickle_file, "rb"))
data = fixu_san(data)
json.dump(data, codecs.open(pickle_file.replace(".bin",".json"), "w", encoding="utf-8"))