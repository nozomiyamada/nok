from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import unquote
import re, csv, os

import date

def tweet_random(month, append=True, scroll=20, sleep_time=0.5):
    """
    month: date.month2013_10 = ['2013-10-1', '2013-10-2',...]
    month[0].rsplit('-', 1) = ['2013-10', '1']
    """
    driver = webdriver.Chrome()
    sleep(1)
    path = '/Users/Nozomi/files/tweet/tweet' + month[0].rsplit('-', 1)[0]
    if not os.path.isdir(path):
        os.makedirs(path)
    
    """
    loop for each day
    last one of data.monthxxx is the 1st day of next month: not iterate
    """
    for i in range(len(month) - 1):

        since = month[i]  # since and until is day: 2015-1-15
        until = month[i]  # if the time is 23:50, override 'until' below

        if append == True:
            # open file once for making tweet ID list
            with open(f'{path}/tweet{since}.tsv', 'r', encoding='utf-8') as f:
                id_list = [line[1] for line in csv.reader(f, delimiter='\t')]

            # open file again for saving tweets in one day
            file = open(f'{path}/tweet{since}.tsv', 'a', encoding='utf-8')
        elif append == False:
            file = open(f'{path}/tweet{since}.tsv', 'w', encoding='utf-8')

        # tsv writer
        writer = csv.writer(file, delimiter='\t', lineterminator='\n')

        # loop for each hour in one day
        for j in range(144):  # date.time = each 10 minute * 24hours

            if j == 143:  # override "since:2013-1-1_23:50:00_ICT until:2013-1-2_0:00:00_ICT"
                until = month[i+1]

            time1 = date.time[j]
            time2 = date.time[j+1]

            # search url: "lang:th since:2013-1-1_15:00:00_ICT until:2013-1-1_15:10:00_ICT"
            url = f'https://twitter.com/search?f=tweets&q=lang%3Ath%20since%3A{since}_{time1}_ICT%20until%3A{until}_{time2}_ICT'
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

            # check banned user
            id_html_checked = [a for a in id_html if ('違反しているため' not in a.text and 'because it violates' not in a.text and 'has been withheld' not in a.text and 'This Tweet is unavailable' not in a.text)]

            for k in range(len(id_html_checked)):
                user_id = id_html_checked[k].get('data-permalink-path').split('/status/')[0].strip('/')
                tweet_id = id_html_checked[k].get('data-permalink-path').split('/status/')[-1]
                tweet = tweet_html[k].text
                
                """ hash tags
                if tweet_html[k].find('a') is not None:
                    hashtags = tweet_html[k].find_all('a')
                    hashtag = [unquote(tag.get('href').split('/hashtag/')[-1].strip('?src=hash')) for tag in hashtags]
                else:
                    hashtag = 'None'
                """
                
                line = [user_id, tweet_id, tweet]
                if append == True:
                    if tweet_id not in id_list:
                        writer.writerow(line)
                else:
                    writer.writerow(line)
        file.close()

    driver.close()


def nok(month, append=True, scroll=8, sleep_time=1, query='นก'):
    """
    month: date.month2013_10 = ['2013-10-1', '2013-10-2',...]
    month[0].rsplit('-', 1) = ['2013-10', '1']
    """
    driver = webdriver.Chrome()
    sleep(1)
    path = '/Users/Nozomi/files/tweet_nok/nok' + month[0].rsplit('-', 1)[0]
    if not os.path.isdir(path):
        os.makedirs(path)
    
    # loop for each day
    for i in range(len(month) - 1):

        since, until = month[i], month[i]  # the same day, if the time is 23:00, override 'until'

        if append == True:
            # open file once for making tweet ID list
            with open(f'{path}/nok{since}.tsv', 'r', encoding='utf-8') as f:
                id_list = [line[1] for line in csv.reader(f, delimiter='\t')]

            # open file again for saving tweets in one day
            file = open(f'{path}/nok{since}.tsv', 'a', encoding='utf-8')
        elif append == False:
            file = open(f'{path}/nok{since}.tsv', 'w', encoding='utf-8')

        # tsv writer
        writer = csv.writer(file, delimiter='\t', lineterminator='\n')

        # loop for every hour in one day
        tweet_one_day = 0  # initialize
        for j in range(48):  # date.time30 = list of 24h

            if j == 47:  # override "since:2013-1-1_23:35:00_ICT until:2013-1-2_0:35:00_ICT"
                until = month[i+1]

            time1 = date.time30[j]
            time2 = date.time30[j+1]

            # search url e.g. "นก since:2013-1-1_16:25:00_ICT until:2013-1-1_17:25:00_ICT"
            url = f'https://twitter.com/search?f=tweets&q={query}%20since%3A{since}_{time1}_ICT%20until%3A{until}_{time2}_ICT'
            driver.get(url)

            # scroll k times
            for t in range(scroll):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll to the bottom
                sleep(sleep_time)

            # scraping
            id_compile = re.compile('tweet js-stream-tweet .*')
            tweet_compile = re.compile('TweetTextSize .*')
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "html.parser")  # get html
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
                if append == True:
                    if tweet_id not in id_list:
                        writer.writerow(line)
                else:
                    writer.writerow(line)

        file.close()

    driver.close()


def sort(year_month_day):  # year_month_day = '2015-1-1'
    year_month = year_month_day.rsplit('-', 1)[0]
    path1 = '/Users/Nozomi/files/tweet_nok/nok{}/nok{}.tsv'.format(year_month, year_month_day)
    path2 = '/Users/Nozomi/files/tweet_nok/nok{}/nok{}_sort.tsv'.format(year_month, year_month_day)
    read_file = open(path1, 'r', encoding='utf-8')
    save_file = open(path2, 'w', encoding='utf-8')
    writer = csv.writer(save_file, delimiter='\t', lineterminator='\n')

    id_list = []
    for line in csv.reader(read_file, delimiter='\t'):
        if line[1] not in id_list:
            writer.writerow(line)
            id_list.append(line[1])

    read_file.close()
    save_file.close()