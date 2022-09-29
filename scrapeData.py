# importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scrapeArticle import get_article
import csv
from datetime import datetime


html = urlopen("https://www.thedailystar.com/")
bs = BeautifulSoup(html,'html.parser')

# Getting all the card-body contains card-labels
card_labels = bs.find_all('div',{'class':'card-labels'})
card_body = []
for card in card_labels:
    card_body.append(card.parent)


# Finding all the NEWS TYPES
news_type = []
for card in card_labels:
    news_type.append(card.div.a.get_text())

# Finding all the headlines
headlines = []
for card in card_body:
    headlines.append(card.find('div',{'class':'card-headline'}).get_text().strip())

# Finding all the urls
urls = []
for card in card_body:
    urls.append(card.find('div',{'class':'card-headline'}).a["href"])



# writing data to a CSV file
filename = "./Daily Data/{}.csv".format(datetime.now().strftime("%Y_%m_%d"))

with open (filename, 'w') as file:
    csv_writer = csv.writer(file)
    for index in range(len(card_labels)-1):
        content = []

        content.append(news_type[index])
        content.append(headlines[index])
        content.append(urls[index])
        csv_writer.writerow(content)