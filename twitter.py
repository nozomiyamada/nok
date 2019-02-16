from time import sleep
from selenium import webdriver
import re
import date
from bs4 import BeautifulSoup
from urllib.parse import unquote
import csv

class Tweet:

    def __init__(self, query):
        self.total_tweeter = set([])
        self.query = query  # e.g. '%23นก'  # hashtag '#' = %23

    """
    example
    
    instantiation: nok = Tweet('%23นก')
    nok.count(date.date2012)
    nok.count(date.date2013)
    ...
    """

    def count(self, period, sleep_time=3):  # period = date.year2013, date.month2013_1
        driver = webdriver.Chrome()
        file2 = open('number.tsv', 'a', encoding='utf-8')
        writer2 = csv.writer(file2, delimiter='\t', lineterminator='\n')

        for i in range(len(period) - 1):

            since = period[i]
            until = period[i+1]

            file1 = open('tweet{}.tsv'.format(since), 'w', encoding='utf-8')
            writer1 = csv.writer(file1, delimiter='\t', lineterminator='\n')

            url = "https://twitter.com/search?f=tweets&q={}%20since%3A{}%20until%3A{}".format(self.query, since, until)
            #url_with_lang = "https://twitter.com/search?f=tweets&q={}%20since%3A{}%20until%3A{}%20lang%3Ath".format(self.query, since, until)

            driver.get(url)
            scroll_list = [0, 1, 2, 3, 4, 5]
            while scroll_list[-1] != scroll_list[-6]:  # if scrolling is not finished, continue
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll to the bottom
                scroll_list.append(driver.execute_script("return document.body.scrollHeight;"))  # get scroll height
                sleep(sleep_time)

            id_compile = re.compile('tweet js-stream-tweet .*')
            date_compile = re.compile('_timestamp .*')
            tweet_compile = re.compile('TweetTextSize .*')

            soup = BeautifulSoup(driver.page_source, "html.parser")  # get html
            id_html = soup.find_all('div', class_=id_compile)  # get user id and tweet id
            date_html = soup.find_all('span', class_=date_compile)  # get the date
            tweet_html = soup.find_all('p', class_=tweet_compile)  # get tweet and hash tag

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
                line = [user_id, tweet_id, date, tweet, hashtag]
                writer1.writerow(line)
                all_list.append(line)
            file2.write(since + ' ' + str(len(id_html)))
            file2.write('\n')
            file1.close()


        """
            tweeter = set([i[0] for i in all_list])
            self.total_tweeter = self.total_tweeter | tweeter
            print('\n' + since)
            print('tweet: {}'.format(len(all_list)))
            print('tweeter: {}'.format(len(tweeter)))
            print('total tweeter: {}'.format(len(self.total_tweeter)))
            line = [len(all_list), len(tweeter), len(self.total_tweeter)]
            writer2.writerow(line)
        """


        driver.close()
        file2.close()
nok = Tweet('นก')


