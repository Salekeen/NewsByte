# importing dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scrapeArticle import get_data
import csv
from datetime import datetime

# todays news
html = urlopen('https://www.thedailystar.net/todays-news')
bs = BeautifulSoup(html, 'html.parser')
all_news_urls = set()
table_data = bs.find_all('tr')
for data in table_data:
    all_news_urls.add(data.find('a')['href'])



# # Finding all the top news page urls
# top_news_urls = set()
# html = urlopen('https://www.thedailystar.net/top-news')
# bs = BeautifulSoup(html, 'html.parser')
# for link in bs.findAll('a'):
#     if 'href' in link.attrs:
#         if link.attrs['href'] in all_news_urls:
#             top_news_urls.add(link.attrs['href'])


# top_news_urls = list(top_news_urls)
all_news_urls = list(all_news_urls)


def write_to_csv(url,filename):
    
    with open(filename, 'w+') as file:
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

# writing data to a CSV file
filename_all_news = "./Get Data/Daily Data/all_news_{}.csv".format(
    datetime.now().strftime("%Y_%m_%d"))
# filename_top_news = "./Get Data/Daily Data/top_news_{}.csv".format(
#     datetime.now().strftime("%Y_%m_%d"))

write_to_csv(all_news_urls,filename_all_news)
# write_to_csv(top_news_urls,filename_top_news)


