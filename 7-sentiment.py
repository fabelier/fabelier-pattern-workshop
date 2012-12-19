from pattern.db import Datasheet
from pattern.metrics import avg

# This is just the stuff from 5-annotation.py, without the tests.
# You can bundle it in an application for predicting sentiment in French text.

sentiment = {}
for row in Datasheet.load("sentiment.csv - Sheet 1.csv", headers=True):
    scores = [float(x) for x in row[3:] if x != ""]
    if scores:
        sentiment[row[0]] = avg(scores)
        
for lemma, forms in Datasheet.load("adj-fr.csv"):
    for form in forms.split(","):
        if lemma in sentiment:
            sentiment[form] = sentiment[lemma]

def positive(review, threshold=0.0):
    """ Returns True if the given review is positive,
        based on the average sentiment score of the adjectives in the text.
    """
    score = 0.0
    n = 0
    for w in review.replace("\n", " ").split(" "):
        w = w.lower()
        w = w.strip(",.!?")
        if w in sentiment:
            score += sentiment[w]
            n += 1
    return score / (n or 1) > threshold
    
print positive("tres bon!")
print positive("tres mal!")