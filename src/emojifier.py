import pandas as pd
import json
import numpy as np

results_dir = "../results/"

#scores = pd.read_csv(results_dir + "matrix.csv")

with open(results_dir + "best_emojis.txt", "r") as json_file:
    best_emojis = json.load(json_file)

def emojify(string):
    word_list = string.split()

    for i, word in enumerate(word_list):
        if word in best_emojis.keys():
            best_emoji = best_emojis[word][0]
            confidence = best_emojis[word][1]
            word_list.insert(i + 1, best_emoji)

    return " ".join(word_list)

test_text = "This happened a few weeks ago. My ~6 year old son came running in to my home office the other day and said, demandingly, 'Dad! Kick me!' So I did. Hear me out, please. The kick was a 3/10 on firmness. Not gentle, but not painful. He's a kid, he likes to play fight, and as he's an only child, I feel like I need to provide a bit of rough and tumble so that he can learn boundaries. I also want him to 'lose some battles', and to learn to 'roll with the punches'. Anyway... I performed a front kick whilst making the Bruce Lee Noise. I trust that you know the one. My son recoiled. He looked shocked, sad and disappointed, all rolled into one. He didn't cry,, but it was close. He blurted out 'I said KISS Me!!!' Oops!"

#print("emojifying this: ", test_text)
print(emojify(test_text))
