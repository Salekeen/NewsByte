# importing all the dependencies
import pandas as pd
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers import Stemmer
import csv
from datetime import datetime

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

def write_to_csv(filename, content):
    
    with open(filename, 'a') as file:
        csv_writer = csv.writer(file)
        # csv_writer.writerow(["Headline", "Summary"])
        
        csv_writer.writerow(content)

# writing data to a CSV file
filename = "./Prototype/Daily Data/top_news_{}.csv".format(
    datetime.now().strftime("%Y_%m_%d"))

for index, article in enumerate(articles):
    content = []
    summary = ""
    headline = headlines[index]
    parser = PlaintextParser.from_string(article,Tokenizer("english"))
    for sentence in summerizer(parser.document,2):
        summary += f"{sentence}\n"
    
    content.append(headline)
    content.append(summary)
    write_to_csv(filename,content)
    
    





    