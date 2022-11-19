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
    """
    It takes the last 7 days of data from the database and returns a dataframe
    
    Returns:
      A dataframe with the last 7 days of data.
    """

    df = get_last_n_days_data(n=7)
    df.reset_index(inplace=True)
    return df


def generate_corpus(df):
    """
    1. Load the spaCy language model
    2. For each headline in the dataframe, create a spaCy document
    3. Run TextRank on the document
    4. For each of the top 5 keywords, append it to the corpus
    
    The corpus is a list of keywords
    
    Args:
      df: the dataframe containing the text
    
    Returns:
      A list of keywords
    """

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
    """
    It takes a list of strings (corpus) and returns a list of tuples (word, frequency) sorted by
    frequency
    
    Args:
      corpus: The corpus is the list of documents that you want to analyze.
      n: number of words to return
    
    Returns:
      A list of tuples, where each tuple is a word and its frequency.
    """

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
    """
    It takes a corpus (a collection of text documents), and returns a list of the n most common words in
    the corpus
    
    Args:
      corpus: The corpus is the collection of text that you want to analyze.
      n: the number of words to return
    
    Returns:
      A list of tuples, where each tuple is a word and its frequency.
    """

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
    """
    It takes a corpus (a collection of text documents) as an input, and returns a list of the n most
    common trigrams in the corpus
    
    Args:
      corpus: The corpus is the collection of text that you want to analyze.
      n: number of top words to return
    
    Returns:
      A list of tuples, where each tuple is a word and its frequency.
    """

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
    """
    It takes a dataframe as input, generates a corpus, and then returns the top 20 unigrams, bigrams,
    and trigrams
    
    Args:
      input_df: the dataframe containing the headlines
    
    Returns:
      A JSON object containing the top 20 unigrams, bigrams, and trigrams.
    """
    
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
    """
    It takes a dataframe, runs it through a function, and then writes the output to a database
    """
    
    input_df = get_dataframe()
    data = headlinesKPE(input_df)
    write_to_database.submit(data)


if __name__ == "__main__":
    headlinesKPE_flow()
