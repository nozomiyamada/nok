from time import sleep
from selenium import webdriver
import re
import date
from bs4 import BeautifulSoup
import csv


def nok(month, scroll=2, sleep_time=2):  # month = date.month2013_1
    driver = webdriver.Chrome()

    # loop for each day
    for i in range(len(month) - 1):

        since = month[i]  # the same day, if the time is 23:00, override 'until'
        until = month[i]

        # make file for saving tweets in one day
        file1 = open('nok{}.tsv'.format(since), 'w', encoding='utf-8')
        writer1 = csv.writer(file1, delimiter='\t', lineterminator='\n')

        # record total tweet numbers of each day
        file2 = open('number_nok.tsv', 'a', encoding='utf-8')
        writer2 = csv.writer(file2, delimiter='\t', lineterminator='\n')

        # loop for every 4 other hour in one day (0, 4, 8 ...)
        tweet_one_day = 0  # initialize
        for j in range(6):  # date.time = list of 24h

            time1 = date.time[4 * j]
            time2 = date.time[4 * j + 3]

            # search url e.g. "นก since:2013-1-1_16:25:00_ICT until:2013-1-1_17:25:00_ICT"
            url = "https://twitter.com/search?f=tweets&q=นก%20since%3A{}_{}_ICT%20until%3A{}_{}_ICT".format(since, time1, until, time2)
            driver.get(url)

            # scroll k times
            for t in range(scroll):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll to the bottom
                sleep(sleep_time)

            # scraping
            id_compile = re.compile('tweet js-stream-tweet .*')
            tweet_compile = re.compile('TweetTextSize .*')
            soup = BeautifulSoup(driver.page_source, "html.parser")  # get html
            id_html = soup.find_all('div', class_=id_compile)  # get user id and tweet id
            tweet_html = soup.find_all('p', class_=tweet_compile)  # get tweet and hash tag
            tweet_one_day += len(id_html)

            # check banned user
            id_html_checked = [a for a in id_html if '違反しているため' not in a.text]

            for k in range(len(id_html_checked)):
                user_id = id_html_checked[k].get('data-permalink-path').split('/status/')[0].strip('/')
                tweet_id = id_html_checked[k].get('data-permalink-path').split('/status/')[-1]
                tweet = tweet_html[k].text
                """
                if tweet_html[k].find('a') is not None:
                    hashtags = tweet_html[k].find_all('a')
                    hashtag = [unquote(tag.get('href').split('/hashtag/')[-1].strip('?src=hash')) for tag in hashtags]
                else:
                    hashtag = 'None'
                """
                line = [user_id, tweet_id, tweet]
                writer1.writerow(line)

        file2.write(since + '\t' + str(tweet_one_day))
        file2.write('\n')
        file1.close()
        file2.close()

    driver.close()
