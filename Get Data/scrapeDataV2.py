# importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scrapeArticle import get_article
import csv
from datetime import datetime

# todays news
html = urlopen('https://www.thedailystar.net/todays-news')
bs = BeautifulSoup(html, 'html.parser')
all_news = set()
table_data = bs.find_all('tr')
for data in table_data:
    all_news.add(data.find('a')['href'])


# Finding all the front page urls
front_page_urls = set()
html = urlopen('https://www.thedailystar.net')
bs = BeautifulSoup(html, 'html.parser')
for link in bs.findAll('a'):
    if 'href' in link.attrs:
        if link.attrs['href'] in all_news:
            front_page_urls.add(link.attrs['href'])


front_page_urls = list(front_page_urls)

# writing data to a CSV file
filename = "./Get Data/Daily Data/front-page-urls-{}.csv".format(
    datetime.now().strftime("%Y_%m_%d"))


with open(filename, 'w+') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["URLS","Article"])
    for index in range(len(front_page_urls)-1):
        content = []
        content.append(front_page_urls[index])
        article = get_article(
            "https://www.thedailystar.net{}".format(front_page_urls[index])
        )
        content.append(article)
        csv_writer.writerow(content)
