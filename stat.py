from pythainlp import word_tokenize
import glob
import csv
import re
import collections

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
    files = glob.glob('./tweet_nok2/nok{}/nok*.tsv'.format(year_month))

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


def tokenize_test(filedate):  # 2012-2-15

    filepath = "./tweet_nok2/nok{}/nok{}.tsv".format(filedate.rsplit('-', 1)[0], filedate)
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


def count(year_month):
    # get file names
    files = glob.glob("./tweet_nok2/nok{}/tokenized_*.tsv".format(year_month))

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
        files = glob.glob("./tweet_nok2/nok{}-{}/tokenized_*.tsv".format(year, month))

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
                                if i != len(tweet)-1 and (tweet[i+1] == coll or tweet[i+1] == 'อีกแล้ว'):
                                    count += 1
        #print('{}-{}'.format(year, month) +'\t' + str(count))
        print(count)
