from pattern.db import Datasheet
from pattern.vector import SVM

# STEP FOUR: TRAINING & TESTING A SUPPORT VECTOR MACHINE
# ======================================================

# First thing to do is load our test data.
# Each row has a review text (column 1) and a positive/negative label (column 2).
# Since it was saved as a text file (i.e., a string), 
# we need to convert column 2 back to boolean values:
data = Datasheet.load("books-fr.test.csv")
data.columns[1].map(lambda v: v == "True")

# Machine learning broadly uses two statistical techniques:
# - unsupervised machine learning (= classification), and
# - supervised machine learning (= clustering).
# Supervised machine learning requires human-tailored training examples.
# Human-tailored means that someone has tagged each training example with a class / label / type.
# In our case, the label is True or False (positive review or not?)
# A classifier will then attempt to predict the class for unknown (=unlabeled) examples.
# A fast and robust classification algorithm is included in Pattern: the support vector machine.
# http://www.clips.ua.ac.be/pages/pattern-vector#classification

# Training an SVM is very easy, 
# just give it strings or lists of words and a label as training material:
classifier = SVM()
for review, positive in data[:50]: # Note: 50 training examples is very little data!
    classifier.train(review, type=positive)

# The idea is that similar strings will contain similar words.
# For an unknown example, the SVM examine the words it contains,
# and look for trained examples with similar words.
# The labels of these trained examples are then used to predict
# the label of the unknown example.
# See: Chapter 6 in "Modeling Creativity: Case Studies in Python".
print "Review:", data[51][0]
print "Positive:", data[51][1]
print "Prediction:", classifier.classify(data[51][0])
print

# We can then evaluate how well the classifier performs,
# by comparing the predicted labels to the hand-tailored labels.
# Important! Examples used for training may not be used for testing.

# A "binary classifier" is a classifier that only has two possible labels (e.g., True or False).
# For binary classification, we can calculate precision & recall.
# This is more reliable than a simple accuracy:
# - recall = the percentage of positive reviews recognized,
# - precision = the percentage of predicted positive reviews that *really are* positive.

# Example 1: P 0.50 R 1.00 
# This means that all positive reviews are discovered.
# But also that 50% of the unknown input is labeled as positive is in reality negative.

# Example 2: P 0.90 R 0.65
# This means that only 65% of positive reviews are discovered.
# However, almost no negative reviews (10%) are incorrectly labeled as being positive.

# In some cases, higher precision is more important (e.g., spam detection).
# In other cases, higher recall is more important (e.g., pedophile detection).

# The classmethod SVM.test() takes a dataset for training and testing
# and returns a (accuracy, precision, recall, F1-score)-tuple:
print SVM.test(data, folds=3) # 3 tests with different 66% train / 33% test slices.
print

# You will notice 2 things:
# - it is slow,
# - it only scores around 0.3 P and 0.6 R, which is very poor.
# The average F1-score is around 45%, which is lower than 50% = random guessing!
# The following lines of code preprocess each review,
# stripping all words except adjectives.
# As we will see, this makes the classifier faster and more accurate (P 0.6 R 0.85).

# Load the lexicon of French adjectives.
adjectives = {}
for lemma, forms in Datasheet.load("adj-fr.csv"):
    for form in forms.split(","):
        adjectives[form] = True

def normalize(review):
    """ Returns a list of (lowercase) adjectives from the given string.
        Punctuation marks (,.!?) are stripped from each word.
    """
    review = review.lower()
    review = review.split(" ")
    review = [w.strip(",.!?") for w in review]
    review = [w for w in review if w in adjectives]
    return review

# Observe how a training example becomes a lot smaller:
print normalize(data[51][0])
print

# Observe how precision and recall increase by removing noise:
print SVM.test([(normalize(review), positive) for review, positive in data], folds=10)
print

# Can you think of ways to improve the accuracy?
# - Should we also use nouns or verbs from Lexique?
# - Is there a relation between sentence length and sentiment?
# - Do UPPERCASE words, swear words and exclamation marks matter?
# - Internet slang? OMFG, LOL, :-D, #crap, ...
# - ...
# => Test it! Any strategy that makes the accuracy go up is interesting.
