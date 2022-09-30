# Importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_data(url):
    article = ""
    html = urlopen(url)
    bs = BeautifulSoup(html,'html.parser')
    article_body = bs.find('article')
    paragraphs = article_body.find_all('p')

    for paragraph in paragraphs:
        article+=paragraph.get_text()

    
    headline = article_body.find('h1',{'itemprop':'headline'})
    return article,headline

