# importing all the dependencies

from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers import Stemmer
from load_data import get_last_n_days_data
from write_to_database import write_to_database

def get_data():

    data = get_last_n_days_data(n=1)
    print(data.shape)
    article_id = data['article_id']
    article_body = data['article_body']
    return article_id,article_body


def make_summery():
    article_id,article_body = get_data()
    stemmer = Stemmer("english")
    summerizer = Summarizer(stemmer)
    summeries = []
    for article in article_body:
        summery = ""
        parser = PlaintextParser.from_string(article, Tokenizer("english"))
        for sentence in summerizer(parser.document, 2):
            summery += f"{sentence}\n"
        summeries.append(summery)
    return article_id,summeries


if __name__ == "__main__":
    article_id,summeries = make_summery()
    write_to_database(article_id,summeries)
