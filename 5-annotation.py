from pattern.db import Datasheet
from pattern.metrics import avg, test, agreement

# STEP FIVE: MANUAL ANNOTATION
# ============================

# https://docs.google.com/folder/d/0Bz59SEXKdzxIVUdQY0Y3SHZ1dXM/edit
# I put a file on Google Docs where we can all enter scores for French adjectives.
# For example: parfait = +1.0, bon = +0.6, anglais = +0.0, mal = -0.6, terrible = -1.0, ...

# There are good reasons and less good reasons to do the work of the SVM by hand.
# Good reasons:
# 1) It's nicer to have an XML data set that a binary pickled file.
# 2) The classifier is domain-specific.
#    If it is trained on book reviews, it will do well for book reviews.
#    If it is trained on Twitter messages, it will do well for Twitter messages.
#    A classifier trained on Twitter messages may perform very poorly on book reviews.
#    A lexicon of adjectives and their score "should be" cross-domain.
# Bad reasons:
# 1) Intuitively, we don't trust machines and we think we can do better.

# Load the sentiment lexicon.
sentiment = {}
for row in Datasheet.load("sentiment.csv - Sheet 1.csv", headers=True):
    scores = [float(x) for x in row[3:] if x != ""] # Exclude empty fields.
    if scores:
        sentiment[row[0]] = avg(scores)
# Inherit the score of each adjective to the inflected forms of the adjective.
# If parfait = +1.0, then parfaite = +1.0 and parfaites = +1.0.
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

# Load the testing data.
data = Datasheet.load("books-fr.test.csv")
data.columns[1].map(lambda v: v == "True")

# I quickly annotated the top 50 adjectives and got 
# P 0.56 and R 0.78, which approximates the performance of the SVM.
# We can probably get better scores by annotating more adjectives.
print test(lambda review: positive(review), data)
print

# We can also calculate kappa on the manual annotation scores.
# Kappa is a measurement of agreement or consensus.
# We want to know the general agreement of positive (+1) vs. negative (-1).
# If the agreement is low, that means the sentiment lexicon is biased,
# since the annotators did not agree on all scores.
scores = Datasheet.load("sentiment.csv - Sheet 1.csv", headers=True)
# 1) Cut off the first three columns.
scores = scores[:,3:]
# 2) Remove empty fields (= annotator did not enter a score for this adjective).
scores = [[float(x) for x in row if x != ""] for row in scores]
# 3) Calculate the maximum number of different annotators.
n = max([len(row) for row in scores])
# 4) Keep only rows for which each annotator entered a score.
scores = [row for row in scores if len(row) == n]
# 5) Sum all positive / negative / neutral votes per adjective.
scores = [[len([x for x in row if x  > 0]), 
           len([x for x in row if x  < 0]),
           len([x for x in row if x == 0])] for row in scores]
try:
    print agreement(scores)
except:
    pass

# Can you think of ways to make the positive() function better?
# - Should we do something with exclamation marks? (e.g., "belle" <=> "belle!")
# - Should we do something with adverbs? (e.g., "belle" <=> "tres belle")
# - Should we process emoticons? Verbs? 
# - ...