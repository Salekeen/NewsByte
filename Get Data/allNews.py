"""allows to get all the article urls of top news section of daily star
"""

# importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup
from getData import get_data
import csv
from datetime import datetime


def get_all_news_urls():
    """returns all news articles urls of the current day
    
    Returns
    -------
    set
        a set of all news artcles of the current day
    """

    html = urlopen('https://www.thedailystar.net/todays-news')
    bs = BeautifulSoup(html, 'html.parser')
    all_news_urls = set()
    table_data = bs.find_all('tr')
    for data in table_data:
        all_news_urls.add(data.find('a')['href'])
    return all_news_urls



def write_to_csv(url, filename):
    """Writes data to a CSV file

    Parameters
    ----------
    url : str
        url of the news article
    filename : str
        dirname of where to save the file
    """

    with open(filename, 'w+', newline='') as file:
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


def main():
    """main function of the script
    """
    
    all_news_urls = list(get_all_news_urls())
    filename_all_news = "./Get Data/Daily Data/all_news_{}.csv".format(
        datetime.now().strftime("%Y_%m_%d"))
    write_to_csv(all_news_urls, filename_all_news)


if __name__ == '__main__':
    main()
