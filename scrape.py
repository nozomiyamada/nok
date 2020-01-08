from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import re, csv, os, glob
from date import *

class ScrapeTweet:
    def __init__(self, path, query=None, scroll_time=30):
        """
        request url - use : (%3A) and space (%20)
        https://twitter.com/search?q=query%20parameter1%3Avalue%20parameter2%3Avalue
        """
        self.path = path  # '/Users/Nozomi/files/tweet/'
        self.scroll_time = scroll_time
        if query == None:
            self.url = 'https://twitter.com/search?q=lang%3Ath'
        else:
            self.url = f'https://twitter.com/search?q={query}'

    def scrape_tweet(self, month, start_date=1, times_per_hour=6): # times per hour = 6,3,2,1
        """
        month: month2013_10 = ['2013-10-1', '2013-10-2',...]
        """
        files = sorted(glob.glob(self.path + month[0].rsplit('-',1)[0] + '/*.tsv'))
        print(sorted([x.rsplit('/')[-1] for x in files]))
        driver = webdriver.Firefox()

        for day_idx in range(start_date-1, len(month)-1):
            day_since = month[day_idx] 
            day_until = month[day_idx]  # if the time is 23:50, override 'day_to' below

            filename = f'{self.path}{month[0].rsplit("-",1)[0]}/{day_since}.tsv'
            if filename in files: # if exists, append
                # open file once for making tweet ID list
                with open(filename, 'r', encoding='utf-8') as f:
                    tweet_id_exist = [line[1] for line in csv.reader(f, delimiter='\t')]
                write_file = open(filename, 'a', encoding='utf-8')
            else:
                write_file = open(filename, 'w', encoding='utf-8')
                tweet_id_exist = []
            writer = csv.writer(write_file, delimiter='\t', lineterminator='\n')

            # loop for every x minute in one day
            repeat_times = 24 * times_per_hour
            time_list = {1:min60, 2:min30, 3:min20, 6:min10}[times_per_hour]
            for j in range(repeat_times):
                if j == repeat_times - 1:  # override "since:2013-1-1_23:50:00_ICT until:2013-1-2_0:00:00_ICT"
                    day_until = month[day_idx+1]

                time_since, time_until = time_list[j], time_list[j+1]
                url = self.url + f'%20since%3A{day_since}_{time_since}_ICT%20until%3A{day_until}_{time_until}_ICT'
                driver.get(url)

                # scroll k times
                scrollheight = []
                for t in range(self.scroll_time):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll to the bottom
                    scrollheight.append(driver.execute_script("return document.body.scrollHeight;"))
                    sleep(1)
                    if len(scrollheight) >= 3 and len(set(scrollheight[-3:])) == 1:
                        break

                # scraping
                id_compile = re.compile('tweet js-stream-tweet .*')
                tweet_compile = re.compile('TweetTextSize .*')
                html = driver.page_source.encode('utf-8')
                soup = BeautifulSoup(html, "html.parser")  # get html
                id_html = soup.find_all('div', class_=id_compile)  # get user id and tweet id
                tweet_html = soup.find_all('p', class_=tweet_compile)  # get tweet and hash tag
                """ hash tags
                if tweet_html[k].find('a') is not None:
                    hashtags = tweet_html[k].find_all('a')
                    hashtag = [unquote(tag.get('href').split('/hashtag/')[-1].strip('?src=hash')) for tag in hashtags]
                else:
                    hashtag = 'None'
                """

                # check banned tweet
                id_html_checked = [a for a in id_html if ('because it violates' not in a.text and 'has been withheld' not in a.text and 'This Tweet is unavailable' not in a.text)]
                for k in range(len(id_html_checked)):
                    user_id = id_html_checked[k].get('data-permalink-path').split('/status/')[0].strip('/')
                    tweet_id = id_html_checked[k].get('data-permalink-path').split('/status/')[-1]
                    tweet = tweet_html[k].text
                    line = [user_id, tweet_id, tweet]
                    if tweet_id not in tweet_id_exist:
                        writer.writerow(line)

            write_file.close()
        driver.close()


### instantiation ###

# scrape tweets that contain "nok"
# for mac
nok = ScrapeTweet('/Users/Nozomi/gdrive/scraping/tweet/tweet_nok/', query='นก', scroll_time=30).scrape_tweet
# for windows
nok_w = ScrapeTweet('F:/gdrive/scraping/tweet/tweet_nok/', query='นก', scroll_time=30).scrape_tweet

# scrape random tweets
# for mac
random_tweet = ScrapeTweet('/Users/Nozomi/gdrive/scraping/tweet/random/', scroll_time=30).scrape_tweet
# for windows
random_tweet_w = ScrapeTweet('F:/gdrive/scraping/tweet/random/', scroll_time=30).scrape_tweet


def tweet_nok(month, append=True, scroll=8, sleep_time=1, query='นก'):
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
            id_html_checked = [a for a in id_html if ('because it violates' not in a.text and 'has been withheld' not in a.text and 'This Tweet is unavailable' not in a.text)]
            print(len(id_html_checked, len(tweet_html)))
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


