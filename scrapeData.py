# importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scrapeArticle import get_article


html = urlopen("https://www.thedailystar.com/")
bs = BeautifulSoup(html,'html.parser')

# Getting all the card-body contains card-labels
card_labels = bs.find_all('div',{'class':'card-labels'})
card_body = []
for card in card_labels:
    card_body.append(card.parent)


# Finding all the NEWS TYPES
for card in card_labels:
    print(card.div.a.get_text())

# Finding all the headlines
for card in card_body:
    print(card.find('div',{'class':'card-headline'}).get_text().strip())

# Finding all the urls
for card in card_body:
    print(card.find('div',{'class':'card-headline'}).a["href"])

