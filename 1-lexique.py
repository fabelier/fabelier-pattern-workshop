from pattern.db import Datasheet

# STEP ONE: ACQUIRING LINGUISTIC DATA
# ===================================
# I found this great resource for French we can use, called "Lexique":
# http://www.lexique.org/

# In Pattern, a datasheet is a convenient wrapper for .csv files.
# The file data is imported as a list of rows.
# Each row is a list of fields.
# The datasheet has additional Excel-like methods,
# for rotating the matrix, grouping rows, etc.
# All fields are imported as Unicode
# (which handles some of the hassle in Python for dealing with special characters).
# http://www.clips.ua.ac.be/pages/pattern-db#datasheet

# The fields in the Lexique corpus are separated by tabs.
# The first row is a header with the field labels.
data = Datasheet.load("Lexique380/Bases+Scripts/Lexique380.txt", separator="\t")
#print data[0]
#print data[1]

# For sentiment analysis, we're interested in adjectives.
# Adjectives is how people express emotion or personal opinion.
# This is the general idea, it varies across different languages. 
# For example, in German, sentiment analysis on adjectives 
# seems to produce poor results.
# For French we won't know until we test it.
# http://www.clips.ua.ac.be/sites/default/files/desmedt-subjectivity.pdf

# We'll need:
# - 1st field (1_ortho => "belle"), 
# - 3rd field (3_lemme => "beau"),
# - 4th field (4_cgram => NOM, ADJ, VER, ...),
# - 8th field (8_freqlemlivres => frequency of lemma in books)
adjectives = {} # dictionary of lemma => [frequency, [form1, form2, ...]]
for row in data:
    form, lemma, tag, weight = (
        row[0],
        row[2],
        row[3],
        row[7]
    )
    # The frequency is important.
    # Most languages have tens of thousands of adjectives.
    # We want to start by covering the most frequent ones,
    # and leave the less important ones for later.
    # Most languages have an exponential Zipf-distribution of word occurences.
    if tag == "ADJ":
        if lemma not in adjectives:
            adjectives[lemma] = [0, []]
        adjectives[lemma][0] = float(weight) # Convert string to number.
        adjectives[lemma][1].append(form)
#print adjectives

# We now want to sort the dictionary by frequency.
# The items() method of a Python dictionary returns a list of (key, value)-tuples.
# In our case, (lemma, [frequency, [form1, form2, ...]]), for example:
# ("beau", [620.07, ["beau", "beaux", "belle", "belles"]])
# We'll make a new list with the frequency at the start of each tuple.
# We can then sort the list by frequency.
adjectives = adjectives.items()
adjectives = [(weight, lemma, forms) for lemma, (weight, forms) in adjectives]
adjectives = sorted(adjectives, reverse=True) # Highest-first.
#print adjectives

# We want to save our list of adjectives as a new corpus.
# Something more manageable than 24MB.
# I prefer a new .csv file with two fields: lemma, and forms (comma-separated).
# Adjectives higher up in the list are more frequent,
# we should deal with those first to get a good coverage.
corpus = Datasheet()
for frequency, lemma, forms in adjectives:
    field1 = lemma
    field2 = ",".join(forms) # Collapse list to comma-separated string.
    corpus.append( [field1, field2] )
corpus.save("adj-fr.csv")

# We end up with a 500KB list of words commonly used to express emotion or opinion,
# sorted by how often they occur in books,
# along with their inflected forms (gender/number, such as "belles").
# The top 10 most frequent adjectives are: 
# "tout", "petit", "grand", "seul", "autre", "meme", "bon", "premier", "beau", "jeune", ...
