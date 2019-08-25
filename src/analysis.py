import numpy as np
from nltk.corpus import stopwords
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
    return word in UNICODE_EMOJI


def get_grouped_emojis(word_list, emoji_post):
    
    grouped_emojis = []
    previous_emoji = ""

    for word in word_list[emoji_post:]:
        if is_emoji(word):
            if word != previous_emoji:
                grouped_emojis.append(word)
                previous_emoji = word
            else:
                continue
        else:
            break
    return "".join(grouped_emojis)


def read_initial_scores(results_dir):
    
    files = os.listdir(results_dir)

    best_emojis = {}
    
    if "scores.txt" in files:
        with open(results_dir + "scores.txt", "r") as f:
            scores = json.load(f)
    else:
        scores = {}

    if "analysed.txt" in files:
        with open(results_dir + "analysed.txt", "r") as f:
            analysed_posts = json.load(f)
    else:
        analysed_posts = []

    return scores, best_emojis, analysed_posts

def save_results(results_dir, scores, best_emojis, analysed_posts, analysis_failed):

    with open(results_dir + "scores.txt", "w") as f:
        json.dump(scores, f)
        f.truncate()

    with open(results_dir + "analysed.txt", "w") as f:
        json.dump(analysed_posts, f)
        f.truncate()

    if not analysis_failed:
        with open(results_dir + "best_emojis.txt", "w") as f:
            json.dump(best_emojis, f)
            f.truncate()
    return

def find_best_emojis(scores):

    best_emojis = {}
    for word, emojis in scores.items():
        best = max(emojis, key = emojis.get)
        confidence = emojis[best]
        best_emojis[word] = (best, confidence)
    sorted_tuples = sorted(best_emojis.items(), key = lambda kv: kv[1][1], reverse = True)
    nr_emojis = len(sorted_tuples)
    #sorted_tuples = sorted_tuples[0: int(0.25*nr_emojis)]


    return {i[0]: i[1] for i in sorted_tuples}

def analyse_comment(content, scores, weight):

    stop_words = set(stopwords.words('english')) 

    #clean expressions
    content_split_emoji = get_emoji_regexp().split(content)
    split_whitespace = [substr.split() for substr in content_split_emoji]
    word_list = functools.reduce(operator.concat, split_whitespace)

    #don't seperate based on capitalization
    word_list = [w.lower() for w in word_list if w not in stop_words]
    #print(word_list)

    #make content iterable and clean emojis off words

    previous_emoji = ""

    # a counter of how many emojis it skips after a group of emojis

    skip_words = 0
    
    # stores pairs of word/emoji so that one comment does not contribute the same combo twice
    previously_encountered = {}

    for emoji_pos, word in enumerate(word_list):

        if skip_words > 0:
            skip_words -= 1
            continue

        if is_emoji(word):
            emoji = get_grouped_emojis(word_list, emoji_pos)
            skip_words = len(emoji) - 1
            #avoid spammed emojis screwing the ranking
            if emoji == previous_emoji:
                emoji_pos += 1
                continue
            for i in range(-3, 6):
                # once emoji is located loop back until actual word is found
                if emoji_pos - i not in range(len(word_list)):
                    continue
                prev_word = word_list[emoji_pos - i]
                if not is_emoji(prev_word) and prev_word.isalpha():
                    
                    # avoid double contribution from same comment
                    if (prev_word in previously_encountered.keys() 
                            and previously_encountered[prev_word] == emoji):
                        continue

                    #add to previously encountered combos:
                    previously_encountered[prev_word] = emoji

                    if prev_word in scores.keys():
                        if emoji in scores[prev_word].keys():
                            scores[prev_word][emoji] += weight / abs(i)
                        else:
                            scores[prev_word][emoji] = weight / abs(i)
                    else:
                        #print("previous: ", scores)
                        scores[prev_word] = {emoji: weight / abs(i)}
                        #print("post: ", scores)
                        previous_emoji = emoji

    return scores

def analyse(posts_dir, results_dir, chunk_size = None):

    # Scores is a dataframe where columns are emojis, rows are words and their crossing is the score
    scores, best_emojis, analysed_posts = read_initial_scores(results_dir)
    to_analyse = [fname for fname in os.listdir(posts_dir) if fname not in analysed_posts]
    analysis_failed = False

    #progress bar
    i = 0
    total_posts = len(to_analyse)

    #try:
    # if chunk size is left undefined, analyse all files that have not been analysed
    if not chunk_size:
        chunk_size = len(to_analyse)

    print("left to analyse: ", chunk_size)

    for i, fname in enumerate(to_analyse[0:chunk_size]):
        print(i/chunk_size * 100, "%")

        analysed_posts.append(fname)
        if os.stat(posts_dir + fname).st_size > 5e5: continue #skip massive files (spam)

        # read comments
        comments = get_comments(posts_dir + fname)

        #filter out negative upvotes and 0's
        comments = [c for c in comments if int(c["ups"]) > 0]
        
        # analyse comments
        for comment in comments:
            weight = get_weight(comment["ups"])
            content = comment["body"]

            # updates scores matrix
            scores = analyse_comment(content, scores, weight)


    print("unique words analysed: ", len(scores))
    best_emojis = find_best_emojis(scores)

    #except:
    #print("ANALYSIS HAS FAILED")
    #analysis_failed = True

    #finally:
    save_results(results_dir, scores, best_emojis, analysed_posts, analysis_failed)



