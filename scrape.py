from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re, csv, os, glob, tqdm
from date import *

class ScrapeTweet:
    def __init__(self, path, query=None, times_per_hour=6, scroll_time=30):
        """
        request url - use : (%3A) and space (%20)
        https://twitter.com/search?q=query%20parameter1%3Avalue%20parameter2%3Avalue
        """
        self.path = path  # '/Users/Nozomi/files/tweet/'
        self.times_per_hour = times_per_hour
        self.scroll_time = scroll_time
        if query == None:
            self.url = 'https://twitter.com/search?q=lang%3Ath'
        else:
            self.url = f'https://twitter.com/search?q={query}'

    def scrape_tweet(self, month, start_date=1): # times per hour = 6,3,2,1
        """
        month: month2013_10 = ['2013-10-1', '2013-10-2',...]
        """
        files = sorted(glob.glob(self.path + month[0].rsplit('-',1)[0] + '/*.tsv'))
        print(sorted([x.rsplit('/')[-1] for x in files]))
        #options = Options()
        #options.add_argument('-headless')
        #driver = webdriver.Firefox(firefox_options=options)
        driver = webdriver.Firefox()

        for day_idx in tqdm.tqdm(range(start_date-1, len(month)-1), desc='day'):
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
            repeat_times = 24 * self.times_per_hour
            time_list = {1:min60, 2:min30, 3:min20, 6:min10}[self.times_per_hour]
            for j in tqdm.tqdm(range(repeat_times), desc='time'):
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
                html = driver.page_source.encode('utf-8')
                soup = BeautifulSoup(html, "html.parser")  # get html
                contents = soup.find_all('li',class_="js-stream-item stream-item stream-item")
                times = [x.small.a.get('title') for x in contents]
                ids = [x.find('div', class_="stream-item-header").a.get('href')[1:] for x in contents]
                tweets = [x.find('div', class_="js-tweet-text-container").text.strip() for x in contents]
                """ hash tags
                if tweet_html[k].find('a') is not None:
                    hashtags = tweet_html[k].find_all('a')
                    hashtag = [unquote(tag.get('href').split('/hashtag/')[-1].strip('?src=hash')) for tag in hashtags]
                else:
                    hashtag = 'None'
                """

                # check banned tweet
                #id_html_checked = [a for a in id_html if ('because it violates' not in a.text and 'has been withheld' not in a.text and 'This Tweet is unavailable' not in a.text)]
                for k in range(len(times)):
                    line = [times[k], tweetids[k], ids[k], tweets[k]]
                    if tweetids[k] not in tweet_id_exist:
                        writer.writerow(line)

            write_file.close()
        driver.close()

    def scrape_tweet_day(self, month, start_date=1):
        """
        month: month2013_10 = ['2013-10-1', '2013-10-2',...]
        """
        files = sorted(glob.glob(self.path + month[0].rsplit('-',1)[0] + '/*.tsv'))
        print(sorted([x.rsplit('/')[-1] for x in files]))
        #options = Options()
        #options.add_argument('-headless')
        #driver = webdriver.Firefox(firefox_options=options)
        driver = webdriver.Firefox()

        for day_idx in tqdm.tqdm(range(start_date-1, len(month)-1), desc='day'):
            day_since = month[day_idx] 
            day_until = month[day_idx+1]  # if the time is 23:50, override 'day_to' below

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

            url = self.url + f'%20since%3A{day_since}_0:00_ICT%20until%3A{day_until}_0:00_ICT'
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

    def scrape_from_now(self, filename):
        """
        month: month2013_10 = ['2013-10-1', '2013-10-2',...]
        """
        #options = Options()
        #options.add_argument('-headless')
        #driver = webdriver.Firefox(firefox_options=options)
        driver = webdriver.Firefox()

        filepath = f'{self.path}/{filename}'
        if os.path.exists(filepath): # if exists, append
            # open file once for making tweet ID list
            with open(filepath, 'r', encoding='utf-8') as f:
                tweet_id_exist = [line[1] for line in csv.reader(f, delimiter='\t')]
            write_file = open(filepath, 'a', encoding='utf-8')
        else:
            write_file = open(filepath, 'w', encoding='utf-8')
            tweet_id_exist = []
        writer = csv.writer(write_file, delimiter='\t', lineterminator='\n')

        url = self.url
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

if os.name == 'nt': # for windows
    nok = ScrapeTweet('F:/gdrive/scraping/tweet/tweet_nok/', query='นก', times_per_hour=6, scroll_time=30).scrape_tweet
    random_tweet = ScrapeTweet('F:/gdrive/scraping/tweet/random/', times_per_hour=6, scroll_time=30).scrape_tweet
else: # for mac
    nok = ScrapeTweet('/Users/Nozomi/gdrive/scraping/tweet/tweet_nok/', query='นก', times_per_hour=6, scroll_time=30).scrape_tweet
    waitong = ScrapeTweet('/Users/Nozomi/gdrive/scraping/tweet/waitong/', query='วัยทอง', times_per_hour=2, scroll_time=5).scrape_from_now
    random_tweet = ScrapeTweet('/Users/Nozomi/gdrive/scraping/tweet/random/', times_per_hour=6, scroll_time=30).scrape_tweet