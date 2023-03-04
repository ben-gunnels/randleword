import json
import os
from pathlib import Path
new_json = {}
words_list = []
with open("spanish_words.txt", "r") as openfile:
    for i, line in enumerate(openfile):
        new_json[str(i)] = line[:-2]

path = Path("./dictionaries/spanish_words.json")
with open(path, "w") as outfile:
    json.dump(new_json, outfile)

    