import collections
import csv
import glob
import re
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

    return text


def tokenize(year_month):
    # get file names
    files = glob.glob('/Users/Nozomi/files/tweet_nok/nok{}/nok*.tsv'.format(year_month))

    for file in files:
        print(file)
        savename = file.rsplit('/', 1)[0] + '/tokenized_' + file.rsplit('/', 1)[1]
        f = open(file, 'r', encoding='utf-8')
        s = open(savename, 'w', encoding='utf-8')
        tokenized = [word_tokenize(trim(tweet[-1])) for tweet in csv.reader(f, delimiter='\t')]
        writer = csv.writer(s, delimiter='\t', lineterminator='\n')
        writer.writerows(tokenized)
        f.close()
        s.close()


def tokenize_one(filedate):  # 2012-2-15

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
    files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/nok*".format(year_month))
    files2 = glob.glob("/Users/Nozomi/files/tweet/tweet{}/*.tsv".format(year_month))
    tweet_count = 0
    tweet_count2 = 0
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            tweet_count += len(list(csv.reader(f, delimiter='\t')))
    for file in files2:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                tweet_count2 += len(list(csv.reader(f, delimiter='\t')))
        except UnicodeDecodeError:
            pass
    return tweet_count, tweet_count2

def all_tweets(year):
    tweet_count = 0
    tweet_count2 = 0
    for i in range(1,13):
        a, b = count_tweet(year + '-{}'.format(i))
        tweet_count += a
        tweet_count2 += b
    print(tweet_count)
    print(tweet_count2)


def count_col(year_month):
    # get file names
    files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/tokenized_*.tsv".format(year_month))

    count_before = collections.Counter()
    count_after = collections.Counter()

    tweets_b = 0
    tweets_a = 0

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            for tweet in csv.reader(f, delimiter='\t'): # loop for tokenized tweet
                for i, word in enumerate(tweet):
                    if word == 'นก':
                        if len(tweet) == 1:
                            pass
                        elif i == 0:
                            if tweet[i+1] != ' ':
                                count_after[tweet[i+1]] += 1
                                tweets_a += 1
                        elif i == len(tweet)-1:
                            if tweet[i-1] != ' ':
                                count_before[tweet[i-1]] += 1
                                tweets_b += 1
                        else:
                            if tweet[i-1] != ' ':
                                count_before[tweet[i-1]] += 1
                                tweets_b += 1
                            if tweet[i+1] != ' ':
                                count_after[tweet[i + 1]] += 1
                                tweets_a += 1

    print(str(count_before.most_common(30)) +'\t'+ str(tweets_b))
    print(str(count_after.most_common(30)) +'\t'+ str(tweets_a))


def count_word(coll, year, ba=0):  # before=0, after=1

    # loop for month

    count_month = []
    for month in range(1, 13):

        count = 0

        # get file names
        files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}-{}/tokenized_*.tsv".format(year, month))

        # loop for file
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:

                # loop for tweet
                for tweet in csv.reader(f, delimiter='\t'): # loop for tokenized tweet
                    for i, word in enumerate(tweet):
                        if word == 'นก':
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


def mai(year_month):
    """
    function for measuring distance between mai and nok
    """
    # get file names
    files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/tokenized_*.tsv".format(year_month))

    # loop for file

    minus1 = 0
    minus2 = 0

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            for tweet in csv.reader(f, delimiter='\t'): # loop for tokenized tweet
                for i, word in enumerate(tweet):
                    if word == 'นก':
                        if i > 0 and tweet[i-1] == 'ไม่':
                            minus1 += 1
                        if i > 1 and tweet[i-2] == 'ไม่':
                            minus2 += 1
    print(minus1, minus2)


def population(month):  # month = '2016-1'
    
    # make the list of files 
    files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/*.tsv".format(month))
    list_tweeters = []
    for i, file in enumerate(files):
        with open(file, 'r', encoding='utf-8') as f:
            tweeters = set([])
            for tweet in csv.reader(f, delimiter='\t'):
                tweeters.add(tweet[0])
            list_tweeters.append(list(tweeters))
        if i > 0:
            try:
                print(len(list_tweeters[-1]))
                print(len(list_tweeters[-2]) * len(list_tweeters[-1]) / len(set(list_tweeters[-2]).intersection(set(list_tweeters[-1]))))
            except:
                pass



def trim(text):
    text = re.sub(r'([ก-๛a-zA-Z])\1{2}\1+', r'\1', text)
    text = re.sub(r'นกนก(นก)+', 'นกนกนก', text)
    text = re.sub(r'([ก-๛a-zA-Z]+)\1{2}\1+', r'\1', text)

    return text

def tokenize_random(month):  # month = '2015-4'
    # get file names
    files = glob.glob('/Users/Nozomi/files/tweet/tweet{}/tweet*.tsv'.format(month))
    save_file = open('/Users/Nozomi/files/tweet/tweet{}/random_{}.tsv'.format(month, month), 'w', encoding='utf-8')
    writer = csv.writer(save_file, delimiter=' ', lineterminator='\n')

    for file in files:
        print(file)  # print current file
        with open(file, 'r', encoding='utf-8') as f:
            tokenized = [word_tokenize(trim(tweet[-1])) for tweet in csv.reader(f, delimiter='\t')]
            writer.writerows(tokenized)

    save_file.close()


def get_pmi(year_month, window=1):
    """
    function for measuring pmi between mai and nok
    """
    # get file names
    files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/random_*.tsv".format(year_month))

    # loop for file

    nok = 0
    mai = 0
    mainok = 0
    total = 0

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            for tweet in csv.reader(f, delimiter='\t'): # loop for tokenized tweet
                total += 1
                if 'ไม่' in tweet:
                    mai += 1
                if 'นก' in tweet:
                    nok += 1
                for i, word in enumerate(tweet):
                    if word == 'นก':
                        if i >= window and 'ไม่' in tweet[i-window:i]:
                            mainok += 1

    if nok != 0 and mai != 0:
        pmi = (mainok*total/mai/nok)
        print(pmi)
    else:
        print(0)
