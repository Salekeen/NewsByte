# Importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_article(url):
    article = ""
    html = urlopen(url)
    bs = BeautifulSoup(html,'html.parser')
    article_body = bs.find('article')
    paragraphs = article_body.find_all('p')

    for paragraph in paragraphs:
        article+=paragraph.get_text()
    return article



article = get_article("https://www.thedailystar.net/news/bangladesh/news/loadshedding-the-relief-assured-yet-materialise-3131366")
print(article)
