from pattern.db import Datasheet

# APPENDIX: BOOK REVIEWS ADJECTIVE FREQUENCY
# ==========================================

# I put a file on Google Docs where we can all enter scores for French adjectives.
# Each adjective has a column that shows its frequency in positive/negative reviews,
# as a handy lead. This script calculates the frequencies.

data = Datasheet.load("books-fr.csv")
data.columns[1].map(lambda v: float(v))

# We have to make a trade-off about what constitutes as a "positive" review
# and what as a "negative" review. In this setup, I am only looking at reviews
# with star rating ***** or *. Everything else is regarded as "neutral".
# This will give us a rough indicator about which adjectives occur frequently
# in very positive and very negative reviews.

pos = [(review, score) for review, score in data if score == 5]
neg = [(review, score) for review, score in data if score == 1]
neu = [(review, score) for review, score in data if score > 1 and score < 5]

n = min(len(pos), len(neg), len(neu))
data = pos[:n] + neg[:n] + neu[:n]

sentiment = []
for i, (lemma, forms) in enumerate(Datasheet.load("adj-fr.csv")[:2000]):
    pos = 0
    neg = 0
    neu = 0
    for review, score in data:
        review = " " + review.lower() + " "
        review = review.replace("!", " ")
        review = review.replace(".", " ")
        review = review.replace(",", " ")
        for form in forms.split(","):
            form = " " + form + " " # Append a space so " tout " doesn't overlap with "toutes".
            if score == 5:
                pos += review.count(form)
            if score == 1:
                neg += review.count(form)
    # Relativize scores between 0.0-1.0.
    sentiment.append((lemma, 
        "%.2f" % (pos / (float(pos + neg + neu) or 1)), # Percentage ****
        "%.2f" % (neg / (float(pos + neg + neu) or 1))  # Percentage *
    ))
    print i

Datasheet(sentiment).save("sentiment.csv")