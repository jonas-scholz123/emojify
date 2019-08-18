import numpy as np
import pandas as pd
import os
import functools
import operator
import json
from emoji import UNICODE_EMOJI, get_emoji_regexp


def get_comments(fpath):
    with open(fpath, "r") as json_file:
        comments = json.load(json_file)
    return comments

def get_weight(upvotes):
    return 0.2 + np.log2(upvotes)

def is_emoji(word):
    if word in UNICODE_EMOJI:
        return True
    else:
        return False

def analyse_comments(content, scores, weight):

    emoji_pos = 0
    
    #clean expressions
    content_split_emoji = get_emoji_regexp().split(content)
    split_whitespace = [substr.split() for substr in content_split_emoji]
    word_list = functools.reduce(operator.concat, split_whitespace)
    word_list = [w.lower() for w in word_list]

    #make content iterable and clean emojis off words

    previous_emoji = ""

    for word in word_list:
        #don't seperate based on capitalization
        if is_emoji(word):
            emoji = word
            #avoid spammed emojis screwing the ranking
            if emoji == previous_emoji: continue
            for i in range(emoji_pos):
                
                # once emoji is located loop back until actual word is found
                prev_word = word_list[emoji_pos - i]
                if not is_emoji(prev_word) and prev_word.isalpha():
                    #print("previous word: ", prev_word)
                    #print("emoji: ", emoji)
                    if prev_word in scores.index:
                        scores.loc[prev_word, emoji] += weight
                    else:
                        scores.loc[prev_word, emoji] = weight
                        previous_emoji = emoji
                    break

        emoji_pos += 1

    return scores

def read_initial_scores(results_dir):
    
    files = os.listdir(results_dir)

    best_emojis = {}
    
    if "matrix.csv" in files:
        scores = pd.read_csv(results_dir + "matrix.csv", index_col = 0)
        scores = scores.astype(np.float64)
    else:
        scores = pd.DataFrame(columns = UNICODE_EMOJI, dtype = np.float64)

    if "analysed.txt" in files:
        with open(results_dir + "analysed.txt", "r") as f:
            analysed_posts = json.load(f)
    else:
        analysed_posts = []

    return scores, best_emojis, analysed_posts

def analyse(posts_dir = r"../posts/", results_dir = "../results/"):


    # Scores is a dataframe where columns are emojis, rows are words and their crossing is the score
    scores, best_emojis, analysed_posts = read_initial_scores(results_dir)

    to_analyse = [fname for fname in os.listdir(posts_dir) if fname not in analysed_posts]
    
    #progress
    i = 0
    total_posts = len(to_analyse)
    print("left to analyse: ", total_posts)

    try:
        for fname in to_analyse[0:50]:
            print(i/total_posts * 100, "%")

            analysed_posts.append(fname)
            if os.stat(posts_dir + fname).st_size > 5e5: continue

            # read comments
            comments = get_comments(posts_dir + fname)

            #filter out negative upvotes and 0's
            comments = [c for c in comments if int(c["ups"]) > 0]
            
            # analyse comments
            for comment in comments:
                weight = get_weight(comment["ups"])
                content = comment["body"]
                scores = analyse_comments(content, scores, weight)

            i += 1

        for word in scores.index.tolist():
            best = scores.loc[word].idxmax(axis = 1)
            confidence = scores.loc[word, best]
            best_emojis[word] = (best, confidence)
    
        pd.Series(best_emojis).to_csv("../results/best_emojis.csv")
        
        sorted_best_emojis = sorted(best_emojis.items(), key = lambda kv: kv[1][1])
        print(pd.Series(sorted_best_emojis))

    finally:


        scores.to_csv("../results/matrix.csv")
        with open("../results/analysed.txt", "w") as f:
            json.dump(analysed_posts, f)
            f.truncate()

    

analyse()




