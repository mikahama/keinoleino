import nltk
from mikatools import *
print("Downloading wordnet")
nltk.download('wordnet')
nltk.download('omw')

"""
if you see:

[nltk_data] Error loading wordnet: <urlopen error [SSL:
[nltk_data]     CERTIFICATE_VERIFY_FAILED] certificate verify failed:
[nltk_data]     unable to get local issuer certificate (_ssl.c:1091)>

run:

python3 -m mikatools.fix_certs
"""

print("Downloading SemFi into data/SemFi.db from https://zenodo.org/record/1137734")

download_file("https://zenodo.org/record/1137734/files/SemFi.db?download=1", script_path("data/SemFi.db"), show_progress=True)

print("python -m uralicNLP.download -l fin")
from uralicNLP import uralicApi
uralicApi.download("fin")