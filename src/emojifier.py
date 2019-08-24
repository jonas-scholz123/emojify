import pandas as pd

results_dir = "../results/"

scores = pd.read_csv(results_dir + "matrix.csv")

def emojify(string):
    i = 0
    for word in string.split():
        if word in scores.index.tolist():
            emoj
        i += 1



