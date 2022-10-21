"""allows to get all the article urls of top news section of daily star
"""

# importing dependencies
import requests
from bs4 import BeautifulSoup
from getData import get_data
import csv
from datetime import datetime
from prefect import task, flow
from prefect.task_runners import SequentialTaskRunner


@task(
    retries=2,
    retry_delay_seconds=60
)
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


@task(
    retries=2,
    retry_delay_seconds=60
)
def get_top_news_urls(all_news_urls):
    """returns all top news articles urls of the current day
    
    Parameters
    ----------
    all_news_urls : list
        collection of all news articles urls of current day

    Returns
    -------
    set
        a set of all news artcles of the current day
    """

    top_news_urls = set()
    html = requests.get('https://www.thedailystar.net/top-news')
    bs = BeautifulSoup(html.content, 'html.parser')
    for link in bs.findAll('a'):
        if 'href' in link.attrs:
            if link.attrs['href'] in all_news_urls:
                top_news_urls.add(link.attrs['href'])
    return top_news_urls


@task(
    retries=2,
    retry_delay_seconds=60
)
def write_to_csv(url, filename):
    """Writes data to a CSV file

    Parameters
    ----------
    url : str
        url of the news article
    filename : str
        dirname of where to save the file
    """

    with open(filename, 'w+', newline='', encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["URLS", "Headline", "Article"])
        for index in range(len(url)-1):
            content = []
            content.append(url[index])
            article, headline = get_data(
                "https://www.thedailystar.net{}".format(url[index])
            )
            content.append(headline)
            content.append(article)

            csv_writer.writerow(content)


@flow(
    name="Top News Scraper",
    task_runner=SequentialTaskRunner()
)
def top_news_scraper_flow():

    all_news_urls = list(get_all_news_urls())
    top_news_urls = list(get_top_news_urls(all_news_urls))
    filename_top_news = "./Scraper/Data/top_news/top_news_{}.csv".format(
        datetime.now().strftime("%Y_%m_%d"))
    write_to_csv(top_news_urls, filename_top_news)


if __name__ == "__main__":
    top_news_scraper_flow()
