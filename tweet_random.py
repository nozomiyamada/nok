from time import sleep
from selenium import webdriver
import re
import date
from bs4 import BeautifulSoup
from urllib.parse import unquote
import csv


def scrape(month, scroll=10, sleep_time=2):  # month = date.month2013_1
    driver = webdriver.Chrome()

    # loop for each day
    for i in range(len(month) - 1):

        since = month[i]  # the same day, if the time is 23:00, override 'until'
        until = month[i]

        # make file for saving tweets in one day
        file1 = open('tweet{}.tsv'.format(since), 'w', encoding='utf-8')
        writer1 = csv.writer(file1, delimiter='\t', lineterminator='\n')

        # record total tweet numbers of each day
        file2 = open('number.tsv', 'a', encoding='utf-8')
        writer2 = csv.writer(file2, delimiter='\t', lineterminator='\n')

        # loop for each hour in one day
        tweet_one_day = 0  # initialize
        for j in range(24):  # date.time = list of 24h

            if j == 23:  # override "since:2013-1-1_23:00:00_ICT until:2013-1-2_0:00:00_ICT"
                until = month[i+1]

            time1 = date.time[j]
            time2 = date.time[j+1]

            # search url e.g. "lang:th since:2013-1-1_15:00:00_ICT until:2013-1-1_16:00:00_ICT"
            url = "https://twitter.com/search?f=tweets&q=lang%3Ath%20since%3A{}_{}_ICT%20until%3A{}_{}_ICT".format(since, time1, until, time2)
            driver.get(url)

            # scroll k times
            for t in range(scroll):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll to the bottom
                sleep(sleep_time)

            id_compile = re.compile('tweet js-stream-tweet .*')
            date_compile = re.compile('_timestamp .*')
            tweet_compile = re.compile('TweetTextSize .*')

            soup = BeautifulSoup(driver.page_source, "html.parser")  # get html
            id_html = soup.find_all('div', class_=id_compile)  # get user id and tweet id
            date_html = soup.find_all('span', class_=date_compile)  # get the date
            tweet_html = soup.find_all('p', class_=tweet_compile)  # get tweet and hash tag
            tweet_one_day += len(id_html)

            for k in range(len(id_html)):
                user_id = id_html[k].get('data-permalink-path').split('/status/')[0].strip('/')
                tweet_id = id_html[k].get('data-permalink-path').split('/status/')[-1]
                tweet_date = date_html[k].text.replace('月', '/').replace('年', '/').replace('日', '')
                tweet = tweet_html[k].text
                if tweet_html[k].find('a') is not None:
                    hashtags = tweet_html[k].find_all('a')
                    hashtag = [unquote(tag.get('href').split('/hashtag/')[-1].strip('?src=hash')) for tag in hashtags]
                else:
                    hashtag = 'None'
                line = [user_id, tweet_id, tweet_date, tweet, hashtag]
                writer1.writerow(line)

        file2.write(since + '\t' + str(tweet_one_day))
        file2.write('\n')
        file1.close()
        file2.close()

    driver.close()
