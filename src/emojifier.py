import pandas as pd
import re
import json
import numpy as np

results_dir = "../results/"

#scores = pd.read_csv(results_dir + "matrix.csv")

with open(results_dir + "best_emojis.txt", "r") as json_file:
    best_emojis = json.load(json_file)

def emojify(string):
    word_list = string.split()

    for i, word in enumerate(word_list):
        clean_word = re.sub("[\.\?!,]", "", word.lower())
        stop_char = re.findall("[\.\?!,]", word.lower())

        if clean_word in best_emojis.keys():
            best_emoji = best_emojis[clean_word][0]
            confidence = best_emojis[clean_word][1]

            if confidence > 0:
                if not stop_char:
                    word_list.insert(i + 1, best_emoji)
                else:
                    word_list[i] = clean_word
                    word_list.insert(i + 1, best_emoji + stop_char[0])

    return " ".join(word_list)

#test_text = "This happened a few weeks ago. My ~6 year old son came running in to my home office the other day and said, demandingly, 'Dad! Kick me!' So I did. Hear me out, please. The kick was a 3/10 on firmness. Not gentle, but not painful. He's a kid, he likes to play fight, and as he's an only child, I feel like I need to provide a bit of rough and tumble so that he can learn boundaries. I also want him to 'lose some battles', and to learn to 'roll with the punches'. Anyway... I performed a front kick whilst making the Bruce Lee Noise. I trust that you know the one. My son recoiled. He looked shocked, sad and disappointed, all rolled into one. He didn't cry,, but it was close. He blurted out 'I said KISS Me!!!' Oops!"

test_text = "Not sure if this is my FU or my wife’s, but this experience happened yesterday. So my wife and I recently moved to a state where marijuana is legal and I use it mostly for anxiety. Every morning I make my own coffee and I put just a tiny bit of THC liquid to start my day out right, about 10mg. Yesterday, my sweet wife decided to surprise me with breakfast and coffee already made so I could get a little more sleep. I give her a big kiss and grab in on the way out the door and eat on the train on the way to work. I down my coffee and start work. My job requires me to have lots of face to face interactions with multiple people, and I get out on the sales floor start working. After about 15 minutes, I start feeling kinda uncomfortably high. I’m stuttering, having issues focusing on whatever I’m looking at, but I brush it off thinking it’s just peaking, it’ll get better from that point. It didn’t. After about half an hour, I’m not just stoned, I’m blasted. I’m sitting in the bathroom kinda freaking out and it hits me: this is the first time my wife has made me coffee with THC. I text her and ask if she remembers how much of the juice she had put in my coffee. To my horror, she says, “Oh I wasn’t sure how much you usually use so I decided to give you a good day and just pour the rest of the bottle in.” All I could do was laugh. She didn’t know. I never explained it to her. She’s not as experienced in these things. She had spiked my coffee with about 80 mg of THC. At that point I surrendered to the fact that I wasn’t going to be able to work. I managed to hold it together enough to tell a manager I had to go home but as soon as I got on the train, I passed out until it reached the end of the line. After the high had passed, I sat my wife down and gave her a very thorough lesson on dosage. We laughed it off and she promised she wouldn’t send me to work on a spaceship from here on out."

#test_text = "fuck you you stupid bitch"

#print("emojifying this: ", test_text)
print(emojify(test_text))
