# importing all the dependencies
import pandas as pd
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers import Stemmer
import json

# Fetching the data from CSV
data = pd.read_csv(
    "./Get Data/Daily Data/top_news_2022_10_03.csv",
    encoding="cp1252"
)
articles = data['Article']
headlines = data['Headline']

# Initializing the Stemmer
stemmer = Stemmer("english")

# Initializing the Summerizer
summerizer = Summarizer(stemmer)

for index, article in enumerate(articles):
    parser = PlaintextParser.from_string(article,Tokenizer("english"))
    print(headlines[index])
    print()
    for sentence in summerizer(parser.document,2):
        print(sentence)
    print("**************")

    