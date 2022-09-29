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


# # Finding all the NEWS TYPES
# for card in card_labels:
#     print(card.div.a.get_text())

# # Finding all the headlines
# for card in card_body:
#     print(card.find('div',{'class':'card-headline'}).get_text().strip())

# # Finding all the urls
# for card in card_body:
#     print(card.find('div',{'class':'card-headline'}).a["href"])



# writing data to a CSV file
filename = "./Daily Data/{}.csv".format(datetime.now().strftime("%Y_%m_%d"))

with open (filename, 'w') as file:
    csv_writer = csv.writer(file)

    for card in card_labels:
        content = card.div.a.get_text()
        content = bytes(content, 'UTF-8')
        content = content.decode('UTF-8')
        csv_writer.writerow(content)


