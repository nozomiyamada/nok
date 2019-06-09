import collections
import csv
import glob
import re
import random
import os
import numpy as np
from pythainlp import word_tokenize


def trim(text):
    """
    :param text: raw text data of each tweet
    :return: trimmed text data

    if there is repetition of string like 'ยยยยยย'
    trim the string

    trim('อาาาาาาราาาาาายยยยยยย')
    >> อาราย

    if there is repetition of 'นก'
    trim into 3 repeats
    trim('นกนกนกนกนกนก')
    >> นกนกนก
    """
    text = re.sub(r'([ก-๛a-zA-Z])\1{2}\1+', r'\1', text)
    text = re.sub(r'นกนก(นก)+', 'นกนกนก', text)
    text = re.sub(r'([ก-๛a-zA-Z]+)\1{2}\1+', r'\1', text)
    return text


def tokenize_nok(year_month):
    """
    :param year_month: str '2018-1'
    :return: tokenize all tweets in the month and combined into one file
    """
    # get file names
    files = glob.glob('/Users/Nozomi/files/tweet_nok/nok{}/nok*.tsv'.format(year_month))
    save_file = open('/Users/Nozomi/files/processed/nok{}.tsv'.format(year_month, year_month), 'w', encoding='utf-8')
    writer = csv.writer(save_file, delimiter='\t', lineterminator='\n')

    for file in files:
        print(file)  # output current file
        with open(file, 'r', encoding='utf-8') as f:
            tokenized = [word_tokenize(trim(tweet[-1]), keep_whitespace=True) for tweet in csv.reader(f, delimiter='\t')]
            writer.writerows(tokenized)

    save_file.close()

def tokenize_random(month):
    """
    :param year_month: str '2018-1'
    :return: tokenize all tweets in the month and combined into one file
    """
    # get file names
    files = glob.glob('/Users/Nozomi/files/tweet/tweet{}/tweet*.tsv'.format(month))
    save_file = open('/Users/Nozomi/files/processed/random{}.tsv'.format(month, month), 'w', encoding='utf-8')
    writer = csv.writer(save_file, delimiter='\t', lineterminator='\n')

    for file in files:
        print(file)  # output current file
        with open(file, 'r', encoding='utf-8') as f:
            tokenized = [word_tokenize(trim(tweet[-1]), keep_whitespace=True) for tweet in csv.reader(f, delimiter='\t')]
            writer.writerows(tokenized)

    save_file.close()


def tokenize_nok_one(filedate):  # 2012-2-15

    filepath = "/Users/Nozomi/files/tweet_nok/nok{}/nok{}.tsv".format(filedate.rsplit('-', 1)[0], filedate)
    savename = filepath.rsplit('/', 1)[0] + '/tokenized_' + filepath.rsplit('/', 1)[1]
    f = open(filepath, 'r', encoding='utf-8')
    s = open(savename, 'w', encoding='utf-8')
    tokenized = []
    for i, tweet in enumerate(csv.reader(f, delimiter='\t')):
        print(i+1, tweet[0])
        tokenized.append(word_tokenize(trim(tweet[-1])))
    writer = csv.writer(s, delimiter='\t', lineterminator='\n')
    writer.writerows(tokenized)
    f.close()
    s.close()


def count_tweet(year_month):
    """
    :param year_month: str '2018-1'
    :return: the number of tweet nok and random tweet
    """
    files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/nok*".format(year_month))  # tweets contain nok
    files2 = glob.glob("/Users/Nozomi/files/tweet/tweet{}/tweet*".format(year_month))  # random tweet
    tweet_count, tweet_count2 = 0, 0
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            tweet_count += len(list(csv.reader(f, delimiter='\t')))
    for file in files2:
        with open(file, 'r', encoding='utf-8') as f:
                tweet_count2 += len(list(csv.reader(f, delimiter='\t')))
    return tweet_count, tweet_count2


def all_tweets(year):
    """
    all tweet count in the year
    """
    tweet_count, tweet_count2 = 0
    for i in range(1,13):
        a, b = count_tweet(year + '-{}'.format(i))
        tweet_count += a
        tweet_count2 += b
    print('tweet nok: {}'.format(tweet_count))
    print('random tweet: {}'.format(tweet_count2))


def freq(word, year, denominator=10000):  # frequency('เป็น', '2018')
    """
    calculate word frequency from random tweet file
    print word frequency of each month and total count of the year
    """

    all_token, all_count = 0, 0

    # iterate month
    for month in range(1, 13):
        file = "/Users/Nozomi/files/processed/random{0}-{1}.tsv".format(year, month)
        token, count = 0, 0
        with open(file, 'r', encoding='utf-8') as f:
            for tweet in csv.reader(f, delimiter='\t'):  # iterate tokenized tweet
                token += len([x for x in tweet if (x != '\n' and not x.startswith(' '))])  # token in one tweet (except space)
                count += tweet.count(word)
        all_token += token
        all_count += count
        print(count * denominator / token)
    print('\ntotal: {}'.format(all_count * denominator / all_token))
    print('tokens: {}'.format(all_token))


def freq_all(word, denominator=10000):  # frequency('เป็น')
    # iterate year
    for year in range(2014, 2019):
        # iterate month
        if year == 2013:
            for month in range(5, 13):
                file = "/Users/Nozomi/files/processed/random{0}-{1}.tsv".format(year, month)
                token, count = 0, 0
                with open(file, 'r', encoding='utf-8') as f:
                    for tweet in csv.reader(f, delimiter='\t'):  # iterate tokenized tweet
                        token += len([x for x in tweet if (x != '\n' and not x.startswith(' '))])  # token in one tweet (except space)
                        count += tweet.count(word)
                print(count * denominator / token)
        else:
            for month in range(1, 13):
                file = "/Users/Nozomi/files/processed/random{0}-{1}.tsv".format(year, month)
                token, count = 0, 0
                with open(file, 'r', encoding='utf-8') as f:
                    for tweet in csv.reader(f, delimiter='\t'):  # iterate tokenized tweet
                        token += len([x for x in tweet if (x != '\n' and not x.startswith(' '))])  # token in one tweet (except space)
                        count += tweet.count(word)
                print(count * denominator / token)


def col_most(year_month, query='นก'):
    # get file names
    file = "/Users/Nozomi/files/processed/nok{}.tsv".format(year_month)
    #file = "/Users/Nozomi/files/processed/random{}.tsv".format(year_month)

    col_b, col_a = collections.Counter(), collections.Counter()
    count_b, count_a = 0, 0

    with open(file, 'r', encoding='utf-8') as f:
        for tweet in csv.reader(f, delimiter='\t'): # loop for tokenized tweet
            for i, word in enumerate(tweet):
                if word == query:
                    if len(tweet) == 1:  # tweet with only one token
                        pass

                    # initial position
                    elif i == 0:
                        if tweet[i+1] != '\n' and not tweet[i+1].startswith(' '):
                            col_a[tweet[i+1]] += 1
                            count_a += 1

                    # final position
                    elif i == len(tweet)-1:
                        if tweet[i-1] != '\n' and not tweet[i-1].startswith(' '):
                            col_b[tweet[i-1]] += 1
                            count_b += 1
                    else:
                        if tweet[i-1] != '\n' and not tweet[i-1].startswith(' '):
                            col_b[tweet[i-1]] += 1
                            count_b += 1
                        if tweet[i+1] != '\n' and not tweet[i+1].startswith(' '):
                            col_a[tweet[i+1]] += 1
                            count_a += 1

    print(str(col_b.most_common(30)) +'\t'+ str(count_b))
    print(str(col_a.most_common(30)) +'\t'+ str(count_a))

def col_pre(year, query, total=True):
    
    for month in range(1, 13):

        col = 0
        total_col = 0
        file = "/Users/Nozomi/files/processed/nok{0}-{1}.tsv".format(year, month)  # for nok
        #file = "/Users/Nozomi/files/processed/random{0}-{1}.tsv".format(year, month)  # for random

        with open(file, 'r', encoding='utf-8') as f:
            for tweet in csv.reader(f, delimiter='\t'):  # loop for tokenized tweet
                for i, word in enumerate(tweet):
                    if word == 'นก':
                        if i > 0 and tweet[i-1] != '\n' and not tweet[i-1].startswith(' '):
                            total_col += 1
                            if tweet[i-1] == query:
                                col += 1

        if total==True:
            print(total_col, col)
        else:
            print(col)
            
def col_fol(year, query, total=True):
    
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


def search_col_year(year, query1, query2):

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


def count_word(coll, year, ba=0, query='นก'):  # before=0, after=1

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


def population(query1='ไม่', query2='นก'):  # month = '2016-1'

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

def recapture(year_month):
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

def get_pmi(year, query1='ไม่', query2='นก'):
    """
    function for measuring pmi between mai and nok
    """
    for month in range(1, 13):
        # get file names
        file = "/Users/Nozomi/files/tweet/tweet{0}-{1}/random_{0}-{1}.tsv".format(year, month)
        p1, p2, p12, total = 0, 0, 0, 0

        with open(file, 'r', encoding='utf-8') as f:
            for tweet in csv.reader(f, delimiter='\t'): # loop for tokenized tweet
                total += 1
                if query1 in tweet:
                    p1 += 1
                if query2 in tweet:
                    p2 += 1
                for i, word in enumerate(tweet):
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


