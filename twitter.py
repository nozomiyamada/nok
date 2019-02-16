from time import sleep
from selenium import webdriver
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote
import csv

query = 'ไม่นก'
since, until = '2016-4-1', '2016-4-30'
url = "https://twitter.com/search?q={}%20since%3A{}%20until%3A{}".format(query, since, until)

driver = webdriver.Chrome()
driver.get(url)

for i in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll to the bottom
    sleep(2)

id_compile = re.compile('tweet js-stream-tweet .*')
date_compile = re.compile('_timestamp .*')
tweet_compile = re.compile('TweetTextSize .*')

soup = BeautifulSoup(driver.page_source, "html.parser")  # get html
id_html = soup.find_all('div', class_=id_compile)  # get user id and tweet id
date_html = soup.find_all('span', class_=date_compile)  # get the date
tweet_html = soup.find_all('p', class_=tweet_compile)  # get tweet and hash tag
sleep(5)
driver.close()

all_list = []
for i in range(len(id_html)):
    user_id = id_html[i].get('data-permalink-path').split('/status/')[0].strip('/')
    tweet_id = id_html[i].get('data-permalink-path').split('/status/')[-1]
    date = date_html[i].text.replace('月', '/').replace('年', '/').replace('日', '')
    tweet = tweet_html[i].text
    if tweet_html[i].find('a') is not None:
        hashtags = tweet_html[i].find_all('a')
        hashtag = [unquote(tag.get('href').split('/hashtag/')[-1].strip('?src=hash')) for tag in hashtags]
    else:
        hashtag = 'None'
    all_list.append((user_id, tweet_id, date, tweet, hashtag))
