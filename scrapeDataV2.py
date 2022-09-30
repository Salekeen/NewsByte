# importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scrapeArticle import get_article
import csv
from datetime import datetime

# todays news
html = urlopen('https://www.thedailystar.net/todays-news')
bs = BeautifulSoup(html,'html.parser')
all_news = set()
table_data = bs.find_all('tr')
for data in table_data:
    all_news.add(data.find('a')['href'])


# Finding all the front page urls
front_page_urls = set()
html = urlopen('https://www.thedailystar.net')
bs = BeautifulSoup(html,'html.parser')
for link in bs.findAll('a'):
    if 'href' in link.attrs:
        if link.attrs['href'] in all_news:
            front_page_urls.add(link.attrs['href'])

# print(front_page_urls)



# writing data to a CSV file
filename = "./Daily Data/front-page-urls-{}.csv".format(datetime.now().strftime("%Y_%m_%d"))


with open (filename, 'w') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["URLS"])
    # csv_writer.writerow(front_page_urls)
    for url in front_page_urls:
        csv_writer.writerow([url])