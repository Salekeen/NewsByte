"""Helper module for scraper.py to grab data from an article url
"""

# Importing dependencies
import http
from bs4 import BeautifulSoup
import requests
from prefect import task
import time


@task(
    retries=2,
    retry_delay_seconds=60
)
def get_data(urls):
    article_bodies = []
    headlines = []

    for i in range(len(urls)):
        try:
            article = ""
            time.sleep(0.01)
            html = requests.get(
                "https://www.thedailystar.net{}".format(urls[i]))
            bs = BeautifulSoup(html.content, 'html.parser')
            article_body = bs.find('article')
            paragraphs = article_body.find_all('p')

            for paragraph in paragraphs:
                article += paragraph.get_text()
            headline = article_body.find(
                'h1', {'itemprop': 'headline'}).get_text()

            article_bodies.append(article)
            headlines.append(headline)
        except AttributeError:
            print(f"something wrong with this link: {urls[i]}")
        except http.client.HTTPException as e:
            print(e)

    return article_bodies, headlines
