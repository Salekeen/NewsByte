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
# article = get_article("https://www.thedailystar.net/news/local_news/george-takei-to-speak-at-suny-oneonta/article_c0c035f4-3b7a-11ed-bf2b-3fcfde3d01ad.html")
# print(article)
