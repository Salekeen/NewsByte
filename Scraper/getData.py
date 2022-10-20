"""Helper module for scraper.py to grab data from an article url
"""

# Importing dependencies
from bs4 import BeautifulSoup
import requests


def get_data(url):
    """given an url of a news article of returns the article body and headline

    Parameters
    ----------
    url : str
        The url of the desired article
    
    Returns
    -------
    article : str
        the article body
    headline : str
        the headline of the article
    """

    article = ""
    html = requests.get(url)
    bs = BeautifulSoup(html.content, 'html.parser')
    article_body = bs.find('article')
    paragraphs = article_body.find_all('p')

    for paragraph in paragraphs:
        article += paragraph.get_text()

    headline = article_body.find('h1', {'itemprop': 'headline'}).get_text()
    return article, headline
