# Installing dependencies
import json
from numpyencoder import NumpyEncoder

import textacy
import pandas as pd
from textacy.extract import keyterms as kt
from sklearn.feature_extraction.text import CountVectorizer

from prefect import task, flow
from prefect.task_runners import SequentialTaskRunner

from load_data import get_last_n_days_data
from write_to_database import write_to_database


@task(
    retries=2,
    retry_delay_seconds=60
)
def get_dataframe():

    df = get_last_n_days_data(n=7)
    df.reset_index(inplace=True)
    return df


def generate_corpus(df):

    corpus = []
    en = textacy.load_spacy_lang("en_core_web_sm", disable=("parser",))
    for index in range(len(df)):
        doc = textacy.make_spacy_doc(df['headline'][index], lang=en)
        output = kt.textrank(
            doc,
            normalize="lemma",
            window_size=10,
            edge_weighting="count",
            position_bias=True,
            topn=5,
        )
        for i in range(len(output)):
            corpus.append(output[i][0])
    return corpus


def get_top_n_words(corpus, n=None):

    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)

    sum_words = bag_of_words.sum(axis=0)

    words_freq = [
        (word, sum_words[0, idx]) for word, idx in
        vec.vocabulary_.items()
    ]
    words_freq = sorted(words_freq, key=lambda x: x[1],
                        reverse=True)
    return words_freq[:n]


def get_top_n2_words(corpus, n=None):

    vec1 = CountVectorizer(ngram_range=(2, 2),
                           max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                  vec1.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1],
                        reverse=True)
    return words_freq[:n]


def get_top_n3_words(corpus, n=None):

    vec1 = CountVectorizer(ngram_range=(3, 3),
                           max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                  vec1.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1],
                        reverse=True)
    return words_freq[:n]


@task(
    retries=2,
    retry_delay_seconds=60
)
def headlinesKPE(input_df):
    kpe = {}

    corpus = generate_corpus(input_df)
    kpe["top_unigrams"] = get_top_n_words(corpus, n=20)
    kpe["top_bigrams"] = get_top_n2_words(corpus, n=20)
    kpe["top_trigrams"] = get_top_n3_words(corpus, n=20)
    # using NumpyEncoder as json doesnt support numpy encoding by default
    data = json.dumps(kpe, cls=NumpyEncoder)
    return data


@flow(
    name="headlinesKPE",
    task_runner=SequentialTaskRunner()
)
def headlinesKPE_flow():
    input_df = get_dataframe()
    data = headlinesKPE(input_df)
    write_to_database.submit(data)


if __name__ == "__main__":
    headlinesKPE_flow()
