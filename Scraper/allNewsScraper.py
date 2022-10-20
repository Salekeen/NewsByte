"""allows to get all the article urls of top news section of daily star
"""

# importing dependencies
from bs4 import BeautifulSoup
from getData import get_data
import csv
from datetime import datetime
import requests
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
    name="All News Scraper",
    task_runner=SequentialTaskRunner()
)
def all_news_scraper_flow():
    all_news_urls = list(get_all_news_urls())
    filename_all_news = "./Scraper/Data/all_news/all_news_{}.csv".format(
        datetime.now().strftime("%Y_%m_%d"))
    write_to_csv(all_news_urls, filename_all_news)


if __name__ == '__main__':
    all_news_scraper_flow()
