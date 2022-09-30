# importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scrapeArticle import get_data
import csv
from datetime import datetime

# todays news
html = urlopen('https://www.thedailystar.net/todays-news')
bs = BeautifulSoup(html, 'html.parser')
all_news = set()
table_data = bs.find_all('tr')
for data in table_data:
    all_news.add(data.find('a')['href'])

print(all_news)


# Finding all the front page urls
front_page_urls = set()
html = urlopen('https://www.thedailystar.net')
bs = BeautifulSoup(html, 'html.parser')
for link in bs.findAll('a'):
    if 'href' in link.attrs:
        if link.attrs['href'] in all_news:
            front_page_urls.add(link.attrs['href'])


front_page_urls = list(front_page_urls)
all_news_urls = list(all_news)

# writing data to a CSV file
filename = "./Get Data/Daily Data/{}.csv".format(
    datetime.now().strftime("%Y_%m_%d"))

with open(filename, 'w+') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["URLS", "Headline", "Article"])
    for index in range(len(all_news_urls)-1):
        content = []
        content.append(all_news_urls[index])
        article, headline = get_data(
            "https://www.thedailystar.net{}".format(all_news_urls[index])
        )
        content.append(headline)
        content.append(article)

        csv_writer.writerow(content)
