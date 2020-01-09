from collections import Counter
import re, os, csv, random, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
plt.style.use('ggplot')
from pythainlp import word_tokenize
from gensim.models import word2vec
from gensim.models import KeyedVectors

class AnalyzeTweet:

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

    def tokenize(self, year_month:str):
        """
        :year_month: '2019-1'
        :return: tokenize all tweets in the month are combined into one file
        [userid, token1, token2, token3,...]
        """
        # get file names
        files = sorted(glob.glob(f'{self.path}/{year_month}/*.tsv')) # /2019-1/2019-1-1.tsv
        save_file = open(f'{self.path}/tokenized/{year_month}.tsv', 'w', encoding='utf-8')
        writer = csv.writer(save_file, delimiter='\t', lineterminator='\n')

        for file in files:
            print(file)  # output current file
            with open(file, 'r', encoding='utf-8') as f:
                tokenized = [[tweet[0]] + word_tokenize(self.trim(tweet[-1]), keep_whitespace=True) for tweet in csv.reader(f, delimiter='\t')]
                writer.writerows(tokenized)
        save_file.close()

    def tweet_month(self, year_month:str):
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

    def tweet_year(self, *years):
        """
        all tweet count in the year
        """
        for year in range(years[0], years[1]+1):
            tweet_count = 0
            for i in range(1,13):
                tweet_count += self.tweet_month(f'{year}-{i}')
            print(f'all tweets of {year}: {tweet_count}')

    def freq(self, year, *queries:str):  # freq(2018, word1, word2...)
        """
        :*args: query words
        calculate word frequency from random tweet file
        print word frequency of each month and total count of the year
        """
        denominator=10000
        df = pd.DataFrame(columns=list(queries)*2 + ['tokens']) # empty dataframe
        # iterate month
        for month in range(1, 13):
            try:
                filename = f"{self.path}/tokenized/{year}-{month}.tsv"
                token, count = 0, [0] * len(queries)
                with open(filename, 'r', encoding='utf-8') as f:
                    for tweet in csv.reader(f, delimiter='\t'):  # iterate tokenized tweet
                        token += len([x for x in tweet[1:] if x not in ['\n','',' ','  ','   ']])  # token in one tweet (except space)
                        for i, word in enumerate(queries):
                            count[i] += tweet.count(word)
                df.loc[f'{year}-{month}'] = count + [c*denominator/token for c in count] + [token]
            except:
                pass
        print(df)

    def bigram_most(self, year, topn=20, query='นก'):
        for month in range(1, 13):
            filename = f"{self.path}/tokenized/{year}-{month}.tsv"
            col_before, col_after = Counter(), Counter()
            count_before, count_after = 0, 0
            with open(filename, 'r', encoding='utf-8') as f:
                for tweet in csv.reader(f, delimiter='\t'): # iterate tokenized tweet
                    tweet = tweet[1:]  # remove userid
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
            print(f'\n{year}-{month} before: {count_before}')
            print(col_before.most_common(topn))
            print(f'\n{year}-{month} after: {count_after}')
            print(col_after.most_common(topn))

    def plot_col(self, year_from=2013, year_to=2018, before=True, query='นก', words=[]):
        """
        plot_col(2013, 2015, before=True, query='นก', 'ไม่','จะ','ความ')
        """
        df = pd.DataFrame(columns=words)  # empty dataframe for collocations
        for year in range(year_from, year_to+1):  # iterate each year
            for month in range(1, 13):
                filename = f"{self.path}/tokenized/{year}-{month}.tsv"
                col_count = {c:0 for c in words}
                token_count = 0
                with open(filename, 'r', encoding='utf-8') as f:
                    for tweet in csv.reader(f, delimiter='\t'): # iterate tokenized tweet
                        tweet = tweet[1:]  # remove userid
                        if len(tweet) <= 1:  # tweet with only one token
                            continue
                        elif query not in tweet:
                            continue
                        for i, word in enumerate(tweet):  # iterate each word in a tweet
                            if word == query:
                                if i > 0 and before == True:
                                    word_before = tweet[i-1]
                                    if word_before not in ['\n', '', ' ', '  ']:
                                        col_count[word_before] = col_count.get(word_before, 0) + 1
                                        token_count += 1
                                elif i < len(tweet)-1 and before == False:
                                    word_after = tweet[i+1]
                                    if word_after not in ['\n', '', ' ', '  ']:
                                        col_count[word_after] = col_count.get(word_after, 0) + 1
                                        token_count += 1
                df.loc[f'{year}-{month}'] = [col_count[w]*100/token_count for w in words]
        print(df)
        plt.rcParams['font.family'] = 'Ayuthaya'
        plt.plot(df)
        plt.ylabel('conditional probabiliry [%]')
        if before:
            plt.title(f'Previous Word of {query}')
        else:
            plt.title(f'Following Word of {query}')
        plt.legend(df.columns)
        plt.show()

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

    def population(self, year_from=2014, year_to=2018, query1='ไม่', query2='นก'):  # month = '2016-1'
        df = pd.DataFrame(columns=['tweeter', 'new', 'total'])
        all_tweeter = set()
        for year in range(year_from, year_to+1):
            for month in range(1, 13):
                filename = f"{self.path}/tokenized/{year}-{month}.tsv"
                with open(filename, 'r', encoding='utf-8') as f:
                    tweeter = set()
                    new_tweeter = set()
                    for tweet in csv.reader(f, delimiter='\t'):
                        for i, word in enumerate(tweet):
                            if i < len(tweet)-1 and word == query1 and tweet[i+1] == query2:
                                tweeter.add(tweet[0])
                                if tweet[0] not in all_tweeter:
                                    all_tweeter.add(tweet[0])
                                    new_tweeter.add(tweet[0])
                df.loc[f'{year}-{month}'] = [len(tweeter), len(new_tweeter), len(all_tweeter)]
        print(df)
        plt.rcParams['font.family'] = 'Ayuthaya'
        plt.plot(df)
        plt.ylabel('number of tweeter')
        plt.title(f'{query1} {query2}')
        plt.legend(df.columns)
        plt.show()

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

    def plot_pmi(self, year_from=2013, year_to=2018, before=True, query='นก', words=[]):
        """
        pmi = log2[p(w1,w2)/p(w1)p(w2)] = log2[c(w1,w2)/c(w1)c(w2) * N] 
        """
        df = pd.DataFrame(columns=words)  # empty dataframe for collocations
        for year in range(year_from, year_to+1):  # iterate each year
            for month in range(1, 13):
                filename = f"{self.path}/tokenized/{year}-{month}.tsv"
                c1, N = 0, 0  # document frequency of query and document number 
                c12, c2 = {w:0 for w in words}, {w:0 for w in words}

                with open(filename, 'r', encoding='utf-8') as f:
                    for tweet in csv.reader(f, delimiter='\t'): # iterate tokenized tweet
                        tweet = tweet[1:]  # remove userid
                        N += 1
                        if query in tweet:
                            c1 += 1
                        for w in words:
                            if w in tweet:
                                c2[w] += 1
                        for i, word in enumerate(tweet): # iterate tokens
                            if word == query:
                                if before and i > 0 and tweet[i-1] in words:
                                    c12[tweet[i-1]] += 1
                                elif before == False and i < len(tweet)-1 and tweet[i+1] in words:
                                    c12[tweet[i+1]] += 1
                                break
                df.loc[f'{year}-{month}'] = [np.log2(bi*N/c1/uni) if c1 != 0 and c2!=0 else np.log2(0) for bi, uni in zip(c12.values(), c2.values())]
        print(df)
        plt.rcParams['font.family'] = 'Ayuthaya'
        plt.plot(df)
        plt.ylabel('PMI')
        if before:
            plt.title(f'Previous Word of {query}')
        else:
            plt.title(f'Following Word of {query}')
        plt.legend(df.columns)
        plt.show()


### instantiation ###
if os.name == 'nt': # for windows
    NOK = AnalyzeTweet('F:/gdrive/scraping/tweet/tweet_nok')
else:
    NOK = AnalyzeTweet('/Users/Nozomi/gdrive/scraping/tweet/tweet_nok')