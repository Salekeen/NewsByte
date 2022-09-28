# Importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getArticle(url):
    article = ""
    html = urlopen(url)
    bs = BeautifulSoup(html,'html.parser')
    article_body = bs.find('div',{'id':'article-body'})
    paragraphs = article_body.find_all('p')

    for paragraph in paragraphs:
        article+=paragraph.get_text()
    return article



# Testing
article = getArticle("https://www.thedailystar.com/news/local_news/otego-woman-dies-in-crash/article_944d784a-39a6-11ed-8602-2b7ef4267e87.html")
print(article)
