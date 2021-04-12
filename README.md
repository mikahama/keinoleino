# Keinoleino

Keinoleino is an artificially intelligent poet who can write poetry in Finnish automatically. It is a computationally creative system capable of natural language generation in Finnish.

This is a refactored and updated (Python 2 to Python 3) version of the Finnish Poem Generator described in:

Hämäläinen, M. (2018). [Harnessing NLG to create Finnish poetry automatically](https://www.researchgate.net/publication/336445306_Harnessing_NLG_to_Create_Finnish_Poetry_Automatically). In Proceedings of the ninth international conference on computational creativity. Association for Computational Creativity (ACC).

	@inproceedings{hamalainen2018harnessing,
	  title={Harnessing NLG to create Finnish poetry automatically},
	  author={H{\"a}m{\"a}l{\"a}inen, Mika},
	  booktitle={Proceedings of the ninth international conference on computational creativity},
	  year={2018},
	  organization={Association for Computational Creativity (ACC)}
	}

This code used to be very much integrated with the [Poem Machine](https://www.researchgate.net/publication/334118432_Poem_Machine_-_a_Co-creative_NLG_Web_Application_for_Poem_Writing) and it used an old version of HFST, [Syntax maker](https://github.com/mikahama/syntaxmaker) and Omorfi. I have updated the code and it should work as before.

## Installation

	python3 -m pip install -r requirements.txt
	python3 -m keinoleino.download

## Usage

To create a poem about a dog (koira), run:

	from keinoleino import create_poem
	print(create_poem("koira"))
	>> koira, tuo vähä piski
	>> miten kuuliainen on piski?
	>> toivonko minä, kun piski jää ?
	>> olen pikkuinen
	>> vaikka piskit eivät päättäisi valikosta, sinä koittaisit piskiä
	>> oletko normaali?
	>> valikot ovat valikkoja

# Business solutions

<img src="https://rootroo.com/cropped-logo-01-png/" alt="Rootroo logo" width="128px" height="128px">

My company, [Rootroo, offers consulting related to Finnish NLG solutions](https://rootroo.com/). We have a strong academic background in the state-of-the-art AI solutions for every NLP need. Just contact us, we are not a can't-garoo.
