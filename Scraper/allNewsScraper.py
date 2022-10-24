# importing dependencies
from bs4 import BeautifulSoup
from getData import get_data
import requests
from write_to_database import write_to_database

def get_all_news_urls():
    """returns all news articles urls of the current day
    
    Returns
    -------
    set
        a set of all news artcles of the current day
    """

    html = requests.get('https://www.thedailystar.net/todays-news')
    bs = BeautifulSoup(html.content, 'html.parser')
    all_news_urls = set()
    table_data = bs.find_all('tr')
    for data in table_data:
        all_news_urls.add(data.find('a')['href'])
    return all_news_urls

if __name__ == "__main__":
    all_news_urls = list(get_all_news_urls())
    article_bodies,headlines = get_data(all_news_urls)
    write_to_database(headlines,article_bodies,all_news_urls)