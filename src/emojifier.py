import pandas as pd
import json
import numpy as np

results_dir = "../results/"

#scores = pd.read_csv(results_dir + "matrix.csv")

with open(results_dir + "best_emojis.txt", "r") as json_file:
    best_emojis = json.load(json_file)

#best_emojis = pd.read_csv(results_dir + "best_emojis.csv")
print(best_emojis)

def emojify(string):
    word_list = string.split()

    for word, i in enumerate(word_list):
        if word in best_emojis.keys():
            best_emoji = best_emojis[word]
            word_list.insert(i + 1, best_emoji)

    return " ".join(word_list)

test_text = "hello my name is cummy"
print(emojify(test_text))
