from pattern.web import URL, DOM, plaintext
from pattern.db import Datasheet

# STEP TWO: ACQUIRING TEST DATA
# =============================
# For testing, we need real-world data (Twitter messages, book reviews, blog posts, ...)
# Many online reviews use a "star rating": * ** *** **** or *****.
# This is essentially a numeric value from 1-5 (very bad => very good).
# This number is ideal for statistical analysis.
# It basically represents the opinion hidden somewhere in the text.
# If we don't have something like a star rating, we need to tag the data by hand.
# Otherwise we can't analyze how well the algorithm performs.

# There is a big online collection of human opinions:
# http://www.amazon.fr/
# We're not allowed to mine Amazon,
# but since we will only use their reviews for testing we could argue to do it anyway.

# I used the Chrome browser to visit http://www.amazon.fr,
# clicked "Livres" > "Litterature" > "Litterature francaise".
# I end up at a page which displays an overview of popular books.
# Each link in the overview leads to a book page with customer reviews + star rating.
# When I navigate the overview (page 2 and 3), I end up at the following URL's:
# http://www.amazon.fr/s/ref=sr_pg_2?rh=n%3A301061%2Cn%3A%21301130%2Cn%3A301132%2Cn%3A302038&page=2&ie=UTF8&qid=1354668977
# http://www.amazon.fr/s/ref=sr_pg_3?rh=n%3A301061%2Cn%3A%21301130%2Cn%3A301132%2Cn%3A302038&page=3&ie=UTF8&qid=1354669111

# We can throw out the last "ie" and "qid" parts it seems.
# Also, the "current page" is defined by the number in the url, which we can replace with a variable:
def books(i):
    return "http://www.amazon.fr/s/ref=sr_pg_" + str(i) + \
           "?rh=n%3A301061%2Cn%3A%21301130%2Cn%3A301132%2Cn%3A302038&page=" + str(i)

# Try it out by pasting the URL in a browser:
#print books(1)
#print books(2)

# We can use Chrome's Developer Tools to inspect the HTML of the overview page.
# It turns out each link to each book is contained in a <div class="prod"> element.

# In Pattern, the DOM (Document Object Model) is a tree of nested HTML elements,
# along with useful methods to traverse and search the tree.
# http://www.clips.ua.ac.be/pages/pattern-web#DOM
# It is easy to fetch each <div class="prod">:

corpus = Datasheet()

for i in range(45): # How many pages?
    url = books(i+1)
    url = URL(url)
    html = url.download(cached=True) # Cache the HTML source locally.
    for product in DOM(html).by_class("prod"):
        #print product.source

        # The link to each book page looks something like:
        # http://www.amazon.fr/dieux-voyagent-toujours-incognito/dp/2266219154/        
        a = product.by_tag("a")[0]
        a = a.attributes["href"]
        #print a

        # After some searching with Chrome, 
        # I found that there is a page with 10 reviews about this book:
        # http://www.amazon.fr/product-reviews/2266219154/
        # So we want to parse the book id from the first link and mine its reviews page:
        id = a.split("/")[-2]
        reviews = "http://www.amazon.fr/product-reviews/" + id + "/"
        print reviews
        
        # We can use Chrome's Developer Tools to inspect the HTML of the review page.
        # It turns out the reviews are contained in a <table id="productReviews"> element.
        # This table has one row and two columns.
        # Each <div> in the first column is a review.
        # If the table is absent, it means there are no reviews for this book.
        reviews = URL(reviews).download(cached=True, throttle=20) # throttle = delay between crawls
        reviews = DOM(reviews).by_id("productReviews")
        if reviews is not None:
            for review in reviews.by_tag("div"):
                # We use a try-except statement to brute-force it:
                # The <div>'s in the table do not have a class to search for,
                # and there may be other <div>'s in-between, which end up in the except-block. 
                try:
                    # The star rating is <span class="swSprite s_star_5_0 " title="5.0 etoiles sur 5">.
                    score = review.by_class("swSprite")[0]
                    score = score.attributes["title"]
                    score = score.split(" ")[0]
                    score = float(score)
                
                    # The review is contained as plain text in the <div>.
                    text = ""
                    for child in review.children:
                        if child.type == "text":
                            text += child.source + " "
                    text = text.strip()
                    text = plaintext(text) # Remove HTML entities, tags, etc.
                    
                    if text:
                        corpus.append((text, score))
                        print score
                        print text
                        print
                
                except Exception, e:
                    #print e
                    pass

        # Now and then, save the corpus of (review, score) items as a .csv file.
        corpus.save("books-fr.csv")
        
# Can you think of other test data to mine for?
# Can you see why it would be useful to have different test sets?
# - Instead of book reviews + star rating, how about tweets + #win or #fail hashtag?
# - How about hotel reviews + star rating from http://fr.hotels.com?
# - ...