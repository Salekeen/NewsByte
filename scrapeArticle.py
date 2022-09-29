# Importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_article(url):
    article = ""
    html = urlopen(url)
    bs = BeautifulSoup(html,'html.parser')
    article_body = bs.find('div',{'id':'article-body'})
    paragraphs = article_body.find_all('p')

    for paragraph in paragraphs:
        article+=paragraph.get_text()
    return article



# Testing
# article = get_article("https://www.thedailystar.com/news/state/alzheimers-drug-shows-promise-in-early-results-of-study/article_5eaa4262-7fe2-592c-9c08-bd04dbc87ed3.html")
# print(article)
