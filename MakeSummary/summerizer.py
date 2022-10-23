# importing all the dependencies

import pandas as pd
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers import Stemmer
from load_data import get_last_n_days_data


def get_data():

    data = get_last_n_days_data(n=3)
    articles = data['article']
    headlines = data['headline']
    urls = data['url']
    date_published = data['date_published']
    return urls, headlines, articles, date_published


def make_summery():
    urls, headlines, articles, date_published = get_data()
    stemmer = Stemmer("english")
    summerizer = Summarizer(stemmer)
    summeries = []
    for article in articles:
        summery = ""
        parser = PlaintextParser.from_string(article, Tokenizer("english"))
        for sentence in summerizer(parser.document, 2):
            summery += f"{sentence}\n"
        summeries.append(summery)
    return summeries, urls, headlines, date_published
