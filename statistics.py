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
    text = re.sub(r'([ก-๛a-zA-Z]+)\1{2}\1+', r'\1', text)
    return text


def tokenize_nok(year_month):
    # get file names
    files = glob.glob('/Users/Nozomi/files/tweet_nok/nok{}/nok*.tsv'.format(year_month))
    save_file = open('/Users/Nozomi/files/tweet_nok/nok{}/tokenized_{}.tsv'.format(year_month, year_month), 'w', encoding='utf-8')

    for file in files:
        print(file)
        f = open(file, 'r', encoding='utf-8')
        tokenized = [word_tokenize(trim(tweet[-1]), keep_whitespace=True) for tweet in csv.reader(f, delimiter='\t')]
        writer = csv.writer(save_file, delimiter='\t', lineterminator='\n')
        writer.writerows(tokenized)
        f.close()

    save_file.close()

def tokenize_random(month):  # month = '2015-4'
    # get file names
    files = glob.glob('/Users/Nozomi/files/tweet/tweet{}/tweet*.tsv'.format(month))
    save_file = open('/Users/Nozomi/files/tweet/tweet{}/random_{}.tsv'.format(month, month), 'w', encoding='utf-8')
    writer = csv.writer(save_file, delimiter='\t', lineterminator='\n')

    for file in files:
        print(file)  # print current file
        try:
            with open(file, 'r', encoding='utf-8') as f:
                tokenized = [word_tokenize(trim(tweet[-1]), keep_whitespace=True) for tweet in csv.reader(f, delimiter='\t')]
                writer.writerows(tokenized)
        except UnicodeDecodeError:
            pass

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
    files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/nok*".format(year_month))
    files2 = glob.glob("/Users/Nozomi/files/tweet/tweet{}/tweet*".format(year_month))
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
    print('tweet nok: {}'.format(tweet_count))
    print('random tweet: {}'.format(tweet_count2))


def frequency(word, year, denominator=10000):  # 'เป็น', 2014
    """
    calculate word frequency from random tweet file
    """

    all_tokens = 0
    all_count = 0

    for i in range(1, 13):
        file = "/Users/Nozomi/files/tweet/tweet{0}-{1}/random_{0}-{1}.tsv".format(year, i)
        token, count = 0, 0
        with open(file, 'r', encoding='utf-8') as f:
            for tweet in csv.reader(f, delimiter='\t'):  # loop for tokenized tweet
                token += len([x for x in tweet if (x != '\n' and not x.startswith(' '))])
                count += tweet.count(word)

        all_tokens += token
        all_count += count
        print(count * denominator / token)
    print('\ntotal: {}'.format(all_count * denominator / all_tokens))
    print('tokens: {}'.format(all_tokens))



def col_most(year_month, query = 'นก'):
    # get file names
    files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/tokenized_*.tsv".format(year_month))
    #files = glob.glob("/Users/Nozomi/files/tweet/tweet{}/random*.tsv".format(year_month))

    col_b, col_a = collections.Counter(), collections.Counter()
    count_b, count_a = 0, 0

    for file in files:
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

def col_year(year, col, ba=0):
    # get file names
    #files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/tokenized_*.tsv".format(year_month))

    for i in range(1, 13):

        col_b, col_a = collections.Counter(), collections.Counter()
        count_b, count_a = 0, 0
        file = "/Users/Nozomi/files/tweet_nok/nok{0}-{1}/tokenized_{0}-{1}.tsv".format(year, i)  # for nok
        #file = "/Users/Nozomi/files/tweet/tweet{0}-{1}/random_{0}-{1}.tsv".format(year, i)  # for random

        with open(file, 'r', encoding='utf-8') as f:
            for tweet in csv.reader(f, delimiter='\t'):  # loop for tokenized tweet
                for i, word in enumerate(tweet):
                    if word == 'นก':
                        if len(tweet) == 1:  # tweet with only one token
                            pass

                        # initial position
                        elif i == 0:
                            if tweet[i+1] != '\n' and not tweet[i+1].startswith(' '):
                                col_a[tweet[i+1]] += 1
                                count_a += 1

                        # final position
                        elif i == len(tweet) - 1:
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

        if ba == 0:
            print(count_b, col_b[col])

        else:
            print(count_a, col_a[col])


def search_col_year(year, query1, query2):
    # get file names
    #files = glob.glob("/Users/Nozomi/files/tweet_nok/nok{}/tokenized_*.tsv".format(year_month))

    for i in range(1, 13):
        count = 0
        token = 0
        file = "/Users/Nozomi/files/tweet/tweet{0}-{1}/random_{0}-{1}.tsv".format(year, i)
        with open(file, 'r', encoding='utf-8') as f:
            for tweet in csv.reader(f, delimiter='\t'): # loop for tokenized tweet
                for j, word in enumerate(tweet):
                    if word != '\n' and not word.startswith(' '):
                        token += 1
                    if word == query1:
                        if len(tweet) == 1:
                            pass
                        elif j < len(tweet) - 1 and tweet[j+1] == query2:
                            count += 1
        print('{}-{}: '.format(year, i), '{0}/{1}'.format(count, token))


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



def get_pmi(year_month, query='ไม่'):
    """
    function for measuring pmi between mai and nok
    """
    # get file names
    file = "/Users/Nozomi/files/tweet/tweet{}/random_{}.tsv".format(year_month, year_month)

    # loop for file

    nok = 0
    mai = 0
    mainok = 0
    total = 0

    with open(file, 'r', encoding='utf-8') as f:
        for tweet in csv.reader(f, delimiter='\t'): # loop for tokenized tweet
            total += 1
            if query in tweet:
                mai += 1
            if 'นก' in tweet:
                nok += 1
            for i, word in enumerate(tweet):
                if word == 'นก':
                    #if i > 0 and tweet[i-1] == query:  # for pre
                    if i < len(tweet)-1 and tweet[i+1] == query:  # for fol
                        mainok += 1
                        break

    if nok != 0 and mai != 0:
        pmi = np.log2(mainok*total/mai/nok)
        print(pmi)
        #print(nok, mai, mainok)
    else:
        print(0)
