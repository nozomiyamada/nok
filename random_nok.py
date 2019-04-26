from time import sleep
from selenium import webdriver
import re
import date
from bs4 import BeautifulSoup
from urllib.parse import unquote
import csv
from os import makedirs


def nok(month, scroll=3, sleep_time=0.5):  # month = date.month2013_10
    """
    example:

    month = date.month2013_10 = ['2013-10-1', '2013-10-2',...]
    month[0].rsplit('-', 1) = ['2013-10', '1']
    path = './tweet_nok/nok2013-10'
    """
    driver = webdriver.Firefox()
    sleep(1)
    path = '/Users/Nozomi/files/khan/' + month[0].rsplit('-', 1)[0]
    makedirs(path)

    # loop for each day
    for i in range(len(month) - 1):

        since = month[i]  # the same day, if the time is 23:00, override 'until'
        until = month[i]

        # make file for saving tweets in one day
        file = open('{}/{}.tsv'.format(path, since), 'w', encoding='utf-8')
        writer = csv.writer(file, delimiter='\t', lineterminator='\n')

        # loop for every hour in one day
        tweet_one_day = 0  # initialize
        for j in range(48):  # date.time30 = list of 24h

            if j == 47:  # override "since:2013-1-1_23:35:00_ICT until:2013-1-2_0:35:00_ICT"
                until = month[i+1]

            time1 = date.time30[j]
            time2 = date.time30[j+1]

            # search url e.g. "นก since:2013-1-1_16:25:00_ICT until:2013-1-1_17:25:00_ICT"
            url = "https://twitter.com/search?f=tweets&q=คัน%20since%3A{}_{}_ICT%20until%3A{}_{}_ICT".format(since, time1, until, time2)
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

            # check banned tweet
            id_html_checked = [a for a in id_html if ('違反しているため' not in a.text and 'because it violates' not in a.text and 'has been withheld' not in a.text and 'This Tweet is unavailable' not in a.text)]

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
                writer.writerow(line)

        file.close()

    driver.close()



