Pattern workshop @ Fabelier


You’ll need:
1. Python programming language: http://www.python.org/download/
2. Pattern for Python: http://www.clips.ua.ac.be/pages/pattern
3. A code editor: http://www.barebones.com/products/textwrangler/


If you want the most recent version of Pattern, download the ZIP from GitHub:
https://github.com/clips/pattern


The main documentation page of Pattern provides installation instructions and a short overview of what is possible. The download contains some examples of each submodule, in the examples/ folder. 


The PDF modeling-creativity-6&7.pdf contains more in-depth information about the various submodules in Pattern, and natural language processing in general. This document is for your own personal use, please don’t spread it.


The .py files show a use case for sentiment analysis for French, that is, predicting if a French text has a positive or negative tone. The code uses some data sets mined from Lexique and Amazon.fr. These are also available as .csv files. The code demonstrates how Pattern can be used to mine data from the Web (with pattern.web), some things about natural language processing and machine learning (with pattern.vector), and a short overview of statistical functions in the pattern.metrics package.


Some slides about a previous project for Dutch sentiment analysis are also available.


You can follow along with the .py files, or experiment on your own. If you just want to play, check out the canvas.js visualization module bundled in Pattern: http://www.clips.ua.ac.be/media/canvas/


If you want to help out with the development of Pattern, take a look at the sentiment.csv sheet. Add a column and provide a score (between -1.0 and +1.0) for each word. A negative score means that you think this word has a negative tone (e.g., terrible). A positive score means that you think this word has a positive tone (e.g., heureux).


Contact:
tom@organisms.be