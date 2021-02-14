# -*- coding: utf-8 -*-
__author__ = 'mikahama'
import json
from . import metaphor_maker
from . import comparison_maker
from . import rhetorical_questions
from . import subjective_opinion
from . import semantic_tools
import copy
import re
import os, codecs
import random
from . import noun_tool
from mikatools import *


themes = {"human": ["mies", "nainen", "lapsi", "tyttö", "poika"], "pets": ["kissa", "koira", "kani", "marsu"], "professions": ["poliisi", "vartija", "palomies", "lääkäri", "johtaja", "hoitaja"], "family": ["isä", "äiti", "sisko", "veli"], "nature": ["metsä", "puu", "joki", "meri"], "transport": ["auto", "pyörä", "lentokone", "laiva"], "seasons":["talvi","kesä","kevät","syksy"]}

theme_words = {"human": ["mies", "nainen", "lapsi", "tyttö", "poika", "pää", "jalka", "varvas", "sormi", "suu", "maha", "käsi", "talo", "hattu", "paita"], "pets": ["kissa", "koira", "kani", "marsu", "hevonen", "kala", "luu", "karvapallo", "häntä", "korva", "kirsu", "kuono", "piha", "sänky", "peitto", "peti", "lattia", "häpeä", "käytös"], "professions": ["poliisi", "vartija", "palomies", "lääkäri", "johtaja", "hoitaja", "sairaala", "putka", "paloasema", "yritys", "teko", "hoito", "keino", "pidätys", "lääke"], "family": ["isä", "äiti", "sisko", "veli", "setä", "täti", "mummo", "vaari", "matka", "koti", "loma", "jääkaappi", "televisio", "ilo", "suru", "peli", "leikki"], "nature": ["metsä", "puu", "joki", "meri", "humina", "kauneus", "koivu", "tammi", "laiva", "orava", "kala", "lokki", "kari", "vesi", "tuuli"], "transport": ["auto", "pyörä", "lentokone", "laiva", "tie", "lentokenttä", "polku", "ilma", "polttoaine", "rengas", "kumi", "vauhti", "onnettomuus", "kapteeni"], "seasons":["talvi","kesä","kevät","syksy", "lumi", "pyry", "tuisku", "aurinko", "jää", "loska", "ruska", "helle", "jäätelö", "kukka", "nurmikko", "nuppu"]}


templates = {}

tools = {"metaphor": metaphor_maker.construct_a_metaphor, "comparison": comparison_maker.create_verse,
         "question" : rhetorical_questions.create_verse, "opinion" : subjective_opinion.create_verse,
         "attitude": subjective_opinion.propositional_attitude, "counterfactual": subjective_opinion.counterfactual_verse,
         "tautology": metaphor_maker.create_a_tautology, "person_description": subjective_opinion.adjective_description, "plain_opinion": subjective_opinion.subjective_opinion,
         "paraphrase": semantic_tools.create_paraphrase, "address": semantic_tools.address_interlocutor,
         "relative_verse": semantic_tools.relative_verse}

def _load_templates():
    """
        Method loads poem structure templates from the "templates" folder. More JSON-templates can be specified there
        Runs at start, templates will be stored in a global variable
    """
    global templates
    templates_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
    files_in_dir = os.listdir(templates_path)
    for file_in_dir in files_in_dir:
        if file_in_dir.endswith(".json"):
            f_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/'+file_in_dir)
            template = json.load(codecs.open(f_path, "r", encoding="utf-8"))
            templates[file_in_dir] = template

_load_templates()

def create_poem(noun, template=None, stop_on_exception=False):
    """
    Creates a new poem based on a noun and an optional template template

    :param noun: string "hevonen"
    :param template: dictionary structure representing the template (see JSON files under "templates" folder for reference
    :param stop_on_exception: for debugging, if true an empty string is returned in case of failure.
    :return: a poem "miten hassu on talo?\nTalot ovat taloja"
    """
    while True:
        #In the DB there might be ?-characters that cannot be converted from unicode to string which causes an exception
        #That's why this loop is needed until the words containing broken characters are removed from the DB
        

        #try:
        return create_actual_poem(noun, template)
        #except:
        #    if stop_on_exception:
        #        return ""

def create_actual_poem(noun=None, template=None, noun_list=[], pos_dict=None):
    """
    Creates a new poem. You have to either provide a noun or (a list of nouns and a pos_dict)
    :param noun: string "auto"
    :param template: dictionary structure representing the template (see JSON files under "templates" folder for reference
    :param noun_list: a list of nouns ["auto", "hevonen"]
    :param pos_dict: Dictionary of words grouped based on their POS {"nouns":["auto", "hevonen"], "verbs": ["juosta", "ajaa"]...}
    :return: a poem "miten hassu on talo?\nTalot ovat taloja"
    """
    random.seed()
    if template is None:
        template_k = random.choice(list(templates.keys()))
        template = templates[template_k]
    template = copy.deepcopy(template)
    poem = ""
    if noun is None:
        prev_data = {"noun": random.choice(noun_list)}
    else:
        prev_data = {"noun": noun}
    for key in range(len(template)):
        key = str(key)
        args = template[key]["args"]
        tool = template[key]["verse"]
        requirement = template[key]["require"]
        arg = prev_data[requirement]
        if noun is None:
            args["noun"] = random.choice(noun_list)
        else:
            args["noun"] = arg
        args["pos_dict"] = pos_dict
        output = tools[tool](**args)
        if output is not None:
            prev_data = output
            poem = poem + "\n" + re.sub("\s\s+", " ", prev_data["verse"]).strip()

    return poem

def create_title(noun):
    """
    Creates a title out of a noun, e.g. hassut talot
    :param noun: a string "talo"
    :return: a title "hassut talot"
    """
    while True:
        try:
            tools = [semantic_tools.add_adjective, semantic_tools.paraphrase]
            tool = random.choice(tools)
            title = tool(noun).to_string()
            return title
        except:
            pass


def create_poem_by_theme(theme):
    """
    Creates a poem based on optional theme
    :param theme: a key in the global themes dictionary
    :param user: user name (will be used in the author field, doesn't need to be a real user)
    :return: a structured poem dictionary {"poem": "miten hassu on talo?\nTalot ovat taloja", "theme": "human", "user": "Mika Hämäläinen", "title" : "valkoinen talo"}
    """
    random.seed()
    if theme not in themes:
        theme = random.choice(themes.keys())

    word = random.choice(themes[theme])
    poem = create_poem(word)
    title = create_title(word)
    return {"poem": poem, "title": title}

def create_poem_by_noun(noun):
    """
    Creates a poem based on a noun
    :param noun: a noun "talo"
    :param user: user name (will be used in the author field, doesn't need to be a real user)
    :return: a structured poem dictionary {"poem": "miten hassu on talo?\nTalot ovat taloja", "theme": "human", "user": "Mika Hämäläinen", "title" : "valkoinen talo"}
    """
    poem = create_poem(noun)
    title = create_title(noun)
    return {"poem": poem, "title": title}



#t_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates/poem_template1.json")
#print t_path
#templates = [json.load(codecs.open(t_path, "r", encoding="utf-8")), json.load(codecs.open(t_path.replace("1.json","2.json"), "r", encoding="utf-8")),json.load(codecs.open(t_path.replace("1.json","3.json"), "r", encoding="utf-8")),json.load(codecs.open(t_path.replace("1.json","6.json"), "r", encoding="utf-8"))]
#words = ["mies", "koira", "lampi", "laakso", "kauneus"]
#for word in words:
#    for x in range(10):
#        template = random.choice(templates)
#        print "\n"
#        print create_poem(word, template=template)
#        print "\n"
