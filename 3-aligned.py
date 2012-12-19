from pattern.db import Datasheet

from random import shuffle

# STEP THREE: SETTING UP A TEST FRAMEWORK
# =======================================
# We now have a set of test data (books-fr.csv),
# and a lexicon of adjectives (adj-fr.csv).
# We can use the lexicon to build a sentiment prediction algorithm,
# and evaluate how well it performs on the test data.

data = Datasheet.load("books-fr.csv")
print "number of reviews:", len(data)

# We have 5,444 reviews + score.
# More data = better training material + more reliable testing.
# To set up a test that is statistically solid, we need to "align" the data.
# It is a good idea to remove neutral reviews (= star rating 3),
# and have an equal amount of negative (= star rating 1-2) and positive (= 4-5) reviews.
# This is a form of binary classification:
# Either a review in the test data is positive or it is not.

# Let's look at the distribution of the data:
distribution = {}
for review, score in data:
    score = float(score)
    if score not in distribution:
        distribution[score] = 0
    distribution[score] += 1
    
print "distribution of reviews by star rating:", distribution

# As can be expected, the data is skewed: 519 negative vs. 4,925 positive reviews.
# People tend to give positive reviews more easily.
# If we don't align the data, our test will be biased.
# An algorithm that is good at detecting positive reviews will do very well,
# while in reality in might be very bad at detecting negative reviews
# (for example, it could be predicting *all* test reviews as positive).

aligned = {
    -1: [], 
    +1: []
}
for review, score in data:
    score = float(score)
    if score == 3: # Discard neutral reviews.
        continue
    if score < 3:
        aligned[-1].append(review)
    if score > 3:
        aligned[+1].append(review)
m = min(len(aligned[-1]), len(aligned[+1]))
m = min(m, 500)
aligned[-1] = aligned[-1][:m]
aligned[+1] = aligned[+1][:m]

print "aligned test corpus:"
print len(aligned[-1])
print len(aligned[+1])

# The aligned list contains (review, positive)-tuples,
# where positive is either True or False,
# with an equal amount of True and False reviews:
aligned = [(review, False) for review in aligned[-1]] + \
          [(review, True) for review in aligned[+1]]
shuffle(aligned)

Datasheet(aligned).save("books-fr.test.csv")