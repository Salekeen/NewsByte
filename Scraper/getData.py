"""Helper module for scraper.py to grab data from an article url
"""

# Importing dependencies
from bs4 import BeautifulSoup
import requests


def get_data(urls):
    article_bodies = []
    headlines = []
    for i in range(len(urls)):
        article = ""
        html = requests.get("https://www.thedailystar.net{}".format(urls[i]))
        bs = BeautifulSoup(html.content, 'html.parser')
        article_body = bs.find('article')
        paragraphs = article_body.find_all('p')

        for paragraph in paragraphs:
            article += paragraph.get_text()
        headline = article_body.find('h1', {'itemprop': 'headline'}).get_text()

        article_bodies.append(article)
        headlines.append(headline)

    return article_bodies, headlines
