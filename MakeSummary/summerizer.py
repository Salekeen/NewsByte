# importing all the dependencies
import pandas as pd
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers import Stemmer
import csv

input_filename = "./Get Data/Daily Data/top_news_2022_10_05.csv"
output_filename = "./MakeSummary/Daily Summary/top_news_summary_2022_10_05.csv"


# Fetching the data from CSV
def get_data(filename=input_filename):
    data = pd.read_csv(
        filename,
        encoding="cp1252"
    )
    articles = data['Article']
    headlines = data['Headline']
    urls = data['URLS']
    return urls,headlines,articles


def make_summary():
    urls, headlines, articles = get_data()
    stemmer = Stemmer("english")
    summerizer = Summarizer(stemmer)

    for index, article in enumerate(articles):
        content_for_row = []
        url = urls[index]
        headline = headlines[index]
        summary = ""
        parser = PlaintextParser.from_string(article, Tokenizer("english"))
        for sentence in summerizer(parser.document, 2):
            summary += f"{sentence}\n"

        
        content_for_row.append(url)
        content_for_row.append(headline)
        content_for_row.append(summary)
        
        write_to_csv(content=content_for_row)


def write_to_csv(content,filename=output_filename):
    with open(filename, 'a+', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(content)


if __name__ == '__main__':
    make_summary()
    