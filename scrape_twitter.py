import requests
import json
from bs4 import BeautifulSoup
import csv
import numpy as np
import collections

date2012 = [['2012-1-1', '2012-1-31'],
 ['2012-2-1', '2012-2-29'],
 ['2012-3-1', '2012-3-31'],
 ['2012-4-1', '2012-4-30'],
 ['2012-5-1', '2012-5-31'],
 ['2012-6-1', '2012-6-30'],
 ['2012-7-1', '2012-7-31'],
 ['2012-8-1', '2012-8-31'],
 ['2012-9-1', '2012-9-30'],
 ['2012-10-1', '2012-10-31'],
 ['2012-11-1', '2012-11-30'],
 ['2012-12-1', '2012-12-31']]

date2016 = [['2016-1-1', '2016-1-31'],
 ['2016-2-1', '2016-2-29'],
 ['2016-3-1', '2016-3-31'],
 ['2016-4-1', '2016-4-30'],
 ['2016-5-1', '2016-5-31'],
 ['2016-6-1', '2016-6-30'],
 ['2016-7-1', '2016-7-31'],
 ['2016-8-1', '2016-8-31'],
 ['2016-9-1', '2016-9-30'],
 ['2016-10-1', '2016-10-31'],
 ['2016-11-1', '2016-11-30'],
 ['2016-12-1', '2016-12-31']]


def scrape(since, until):
    query = 'ไม่นก'
    url = "https://twitter.com/search?q={}%20lang%3Ath%20since%3A{}%20until%3A{}".format(query, since, until)
    response = requests.get(url)  # get html
    if response.status_code == 200:  # if 404 pass
        soup = BeautifulSoup(response.text, "html.parser")  # get text
        content_list = soup.find_all('p', class_="TweetTextSize  js-tweet-text tweet-text")
        print(content_list)
