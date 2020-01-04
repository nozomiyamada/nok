from collections import Counter
import re, os, csv, random, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
plt.style.use('ggplot')
from pythainlp import word_tokenize

class TweetAnalyze:

    def __init__(self, path):
        self.path = path  # /Users/Nozomi/files/tweet_nok (/20XX-XX/20XX-XX-X.tsv)
        

    def trim(self, text):
        """
        :param text: raw text data of each tweet
        :return: trimmed text data

        if there is repetition of string like 'ยยยยยย'
        trim the string

        trim('อาาาาาาราาาาาายยยยยยย')
        >> อาราย

        if there is repetition of 'นก'
        trim into 1 repeats
        trim('นกนกนกนกนกนก')
        >> นก
        """
        text = re.sub(r'555+\+?', '555', text)
        text = re.sub(r'([ก-๛a-zA-Z])\1{2}\1+', r'\1', text)
        text = re.sub(r'นก(นก)+', 'นก', text)
        text = re.sub(r'าา+', r'า', text)  # more than 2 repetition
        text = re.sub(r'([ก-๛a-zA-Z]+)\1\1+', r'\1', text)  # more than 3 repetition
        text = re.sub(r'@\S+ ', '', text)
        text = re.sub(r'https?://\S+\b', '', text)
        return text

    def tokenize(self, year_month:str, data_a=True):
        """
        :year_month: '2019-1'
        :return: tokenize all tweets in the month and combined into one file
        """
        # get file names
        files = sorted(glob.glob(f'{self.path}/{year_month}/*.tsv')) # /2019-1/2019-1-1.tsv
        save_file = open(f'{self.path}/tokenized/{year_month}.tsv', 'w', encoding='utf-8')
        writer = csv.writer(save_file, delimiter='\t', lineterminator='\n')

        for file in files:
            print(file)  # output current file
            with open(file, 'r', encoding='utf-8') as f:
                tokenized = [word_tokenize(self.trim(tweet[-1]), keep_whitespace=True) for tweet in csv.reader(f, delimiter='\t')]
                writer.writerows(tokenized)
        save_file.close()

    def count_tweet(self, year_month:str):
        """
        :param year_month:'2018-1'
        :return: the number of tweet nok and random tweet
        """
        files = glob.glob(f'{self.path}/{year_month}/*.tsv') # /2019-1/2019-1-1.tsv
        tweet_count = 0
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                tweet_count += len(list(csv.reader(f, delimiter='\t')))
        return tweet_count

    def count_tweet_all(self, year:int):
        """
        all tweet count in the year
        """
        tweet_count = 0
        for i in range(1,13):
            tweet_count += self.count_tweet(f'{year}-{i}')
        print(f'all tweets of {year}: {tweet_count}')

    def freq(self, year, *args:str):  # freq(2018, word1, word2...)
        """
        :*args: query words
        calculate word frequency from random tweet file
        print word frequency of each month and total count of the year
        """
        denominator=10000

        # iterate month
        for month in range(1, 13):
            filename = f"{self.path}/tokenized/{year}-{month}.tsv"
            token, count = 0, [0] * len(args)
            with open(filename, 'r', encoding='utf-8') as f:
                for tweet in csv.reader(f, delimiter='\t'):  # iterate tokenized tweet
                    token += len([x for x in tweet if x not in ['\n','',' ','  ','   ']])  # token in one tweet (except space)
                    for i, word in enumerate(args):
                        count[i] += tweet.count(word)
            result = ''
            for c in count:
                result += f'{c * denominator / token:.3f},' 
            print(result.strip(','))

    def bigram_most(self, year_month, topn=20, query='นก'):
        filename = f"{self.path}/tokenized/{year_month}.tsv"
        col_before, col_after = Counter(), Counter()
        count_before, count_after = 0, 0
        with open(filename, 'r', encoding='utf-8') as f:
            for tweet in csv.reader(f, delimiter='\t'): # iterate tokenized tweet
                if len(tweet) <= 1:  # tweet with only one token
                    continue
                for i, word in enumerate(tweet):
                    if word == query:
                        # initial position
                        if i == 0:
                            word_after = tweet[i+1]
                            if word_after not in ['\n', '', ' ']:
                                col_after[word_after] += 1
                                count_after += 1
                        elif i == len(tweet)-1:
                            word_before = tweet[i-1]
                            if word_before not in ['\n', '', ' ']:
                                col_before[word_before] += 1
                                count_before += 1
                        else:
                            word_after = tweet[i+1]
                            if word_after not in ['\n', '', ' ']:
                                col_after[word_after] += 1
                                count_after += 1
                            word_before = tweet[i-1]
                            if word_before not in ['\n', '', ' ']:
                                col_before[word_before] += 1
                                count_before += 1
        print(f'before: {count_before}')
        print(col_before.most_common(topn))
        print(f'\nafter: {count_after}')
        print(col_after.most_common(topn))

    def plot_col(self, year_from=2013, year_to=2018, *collocation):
        collocation = sorted(collocation)
        df_before = pd.DataFrame(columns=collocation) # empty dataframe
        df_after = pd.DataFrame(columns=collocation) # empty dataframe
        for year in range(year_from, year_to+1):
            for month in range(1, 13):
                filename = f"{self.path}/tokenized/{year}-{month}.tsv"
                col_before, col_after = {c:0 for c in collocation}, {c:0 for c in collocation}
                count_before, count_after = 0, 0
                with open(filename, 'r', encoding='utf-8') as f:
                    for tweet in csv.reader(f, delimiter='\t'): # iterate tokenized tweet
                        if len(tweet) <= 1:  # tweet with only one token
                            continue
                        for i, word in enumerate(tweet):
                            if word in collocation:
                                # initial position
                                if i == 0:
                                    word_after = tweet[i+1]
                                    if word_after not in ['\n', '', ' ']:
                                        col_after[word][word_after] = col_after[word].get(word_after, 0) + 1
                                        count_after += 1
                                elif i == len(tweet)-1:
                                    word_before = tweet[i-1]
                                    if word_before not in ['\n', '', ' ']:
                                        col_after[word][word_before] = col_after[word].get(word_before, 0) + 1
                                        count_before += 1
                                else:
                                    word_after = tweet[i+1]
                                    if word_after not in ['\n', '', ' ']:
                                        col_after[word][word_after] = col_after[word].get(word_after, 0) + 1
                                        count_after += 1
                                    word_before = tweet[i-1]
                                    if word_before not in ['\n', '', ' ']:
                                        col_after[word][word_before] = col_after[word].get(word_before, 0) + 1
                                        count_before += 1
                df_before.loc[f'{year}-{month}'] = [col_before[q]/count_before for q in query]
                df_after.loc[f'{year}-{month}'] = [col_after[q]/count_after for q in query]
        
        plt.plot(df_before)
        plt.show()

    def col_fol(self, year, query, total=True):
        
        for i in range(1, 13):

            col = 0
            total_col = 0
            file = "/Users/Nozomi/files/processed/nok{0}-{1}.tsv".format(year, i)  # for nok
            #file = "/Users/Nozomi/files/processed/random{0}-{1}.tsv".format(year, i)  # for random

            with open(file, 'r', encoding='utf-8') as f:
                for tweet in csv.reader(f, delimiter='\t'):  # loop for tokenized tweet
                    for i, word in enumerate(tweet):
                        if word == 'นก':
                            if i<len(tweet)-1 and tweet[i+1] != '\n' and not tweet[i+1].startswith(' '):
                                total_col += 1
                                if tweet[i+1] == query:
                                    col += 1

            if total==True:
                print(total_col, col)
            else:
                print(col)


    def search_col_year(self, year, query1, query2):

        for i in range(1, 13):
            count = 0
            token = 0
            file = "/Users/Nozomi/files/processed/random{0}-{1}.tsv".format(year, i)
            with open(file, 'r', encoding='utf-8') as f:
                for tweet in csv.reader(f, delimiter='\t'): # loop for tokenized tweet
                    for j, word in enumerate(tweet):
                        if word != '\n' and not word.startswith(' '):
                            token += 1
                        if word == query1:
                            if j < len(tweet) - 1 and tweet[j+1] == query2:
                                count += 1
            print('{}-{}: '.format(year, i), '{0}\t{1}'.format(count, round(count/token*10000, 2)))


    def count_word(self, coll, year, ba=0, query='นก'):  # before=0, after=1

        # loop for month

        count_month = []
        for month in range(1, 13):

            count = 0

            # get file names
            files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}-{}/tokenized_*.tsv".format(year, month))
            #files = glob.glob("/Users/Nozomi/files/tweet/tweet{}-{}/random_*.tsv".format(year, month))

            # loop for file
            for file in files:
                with open(file, 'r', encoding='utf-8') as f:

                    # loop for tweet
                    for tweet in csv.reader(f, delimiter='\t'): # loop for tokenized tweet
                        for i, word in enumerate(tweet):
                            if word == query:
                                if len(tweet) == 1:
                                    pass
                                elif ba == 0:  # search before word
                                    if i != 0 and tweet[i-1] == coll:
                                        count += 1
                                elif ba == 1: # search after word
                                    if i != len(tweet) - 1 and tweet[i + 1] == coll:
                                    #if i != len(tweet)-1 and (tweet[i+1] == coll or tweet[i+1] == 'อีกแล้ว'):
                                        count += 1
            #print('{}-{}'.format(year, month) +'\t' + str(count))
            print(count)


    def population(self, query1='ไม่', query2='นก'):  # month = '2016-1'

        all_tweeter = set()
        for year in range(2014, 2019):
            for month in range(1, 13):
                file = "/Users/Nozomi/files/tweet_nok/nok{0}-{1}/tokenized_{0}-{1}.tsv".format(year, month)
                with open(file, 'r', encoding='utf-8') as f:
                    tweeter = set()
                    new_tweeter = set()
                    for tweet in csv.reader(f, delimiter='\t'):
                        for i, word in enumerate(tweet):
                            if i < len(tweet)-1 and word == query1 and tweet[i+1] == query2:
                                tweeter.add(tweet[0])
                                if tweet[0] not in all_tweeter:
                                    all_tweeter.add(tweet[0])
                                    new_tweeter.add(tweet[0])
                    print('{}\t{}\t{}'.format(len(tweeter), len(all_tweeter), len(new_tweeter)))

    def recapture(self, year_month):
        #files = glob.glob("/Users/Nozomi/files/tweet/tweet{}/*.tsv".format(year_month))
        files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/*.tsv".format(year_month))

        mark, cap = set(), set()
        pop_list = []
        for i, file in enumerate(files):
            with open(file, 'r', encoding='utf-8') as f:
                user = [tweet[0] for tweet in csv.reader(f, delimiter='\t')]
            cap = set(random.sample(user, 1000))
            recap = mark & cap
            if len(recap) != 0:
                pop = len(cap) * len(mark) / len(recap)
                print(pop)
                pop_list.append(pop)
            else:
                print(0)

            mark = set(random.sample(user, 1000))

        print('mean: {}'.format(np.mean(pop_list)))

    def get_pmi(self, year, query1='ไม่', query2='นก'):
        """
        function for measuring pmi between mai and nok
        """
        for month in range(1, 13):
            # get file names
            file = f"/Volumes/NOZOMIUSB/processed/random{year}-{month}.tsv"
            p1, p2, p12, total = 0, 0, 0, 0

            with open(file, 'r', encoding='utf-8') as f:
                for tweet in csv.reader(f, delimiter='\t'): # iterate tokenized tweet
                    total += 1
                    if query1 in tweet:
                        p1 += 1
                    if query2 in tweet:
                        p2 += 1
                    for i, word in enumerate(tweet): # iterate tokens
                        if word == query1:
                            if i < len(tweet)-1 and tweet[i+1] == query2:
                                p12 += 1
                                break

            if p12 == 0:
                pmi = np.log2(0)
            elif p1 != 0 and p2 != 0:
                pmi = np.log2(p12*total/p1/p2)
            else:
                pmi = np.log2(0)
            print(pmi)


### instantiation ### 
NOK = TweetAnalyze('/Users/Nozomi/files/tweet_nok')