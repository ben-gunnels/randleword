import json
import os

new_json = {}
words_list = []
with open("english_word_dict.json", "r") as openfile:
    json_object = json.load(openfile)


words_list = json_object.keys()

for i, v in enumerate(words_list):
    new_json[i] = v

with open("english_words.json", "w") as outfile:
    json.dump(new_json, outfile)

    