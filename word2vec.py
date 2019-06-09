from pythainlp.tokenize import word_tokenize
from gensim.models import word2vec
from gensim.models import KeyedVectors
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import re
import numpy as np
font = {"family":"Ayuthaya"}
mpl.rc('font', **font)


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


def combine(month):  # month = '2015-4'
    """
    # get file names
    files = glob.glob('/Users/Nozomi/files/tweet/tweet{}/tweet*.tsv'.format(month))
    files_nok = glob.glob('/Users/Nozomi/files/tweet_nok/nok{}/nok*.tsv'.format(month))
    save_file = open('/Users/Nozomi/files/tweet/tweet{}/tokenized_{}.tsv'.format(month, month), 'w', encoding='utf-8')
    writer = csv.writer(save_file, delimiter=' ', lineterminator='\n')

    # tokenize
    for file in files_nok:
        with open(file, 'r', encoding='utf-8') as f:
            print(file)  # print current file
            tokenized = [word_tokenize(trim(tweet[-1])) for tweet in csv.reader(f, delimiter='\t')]
            writer.writerowห(tokenized)

    for file in files:
        print(file)  # print current file
        with open(file, 'r', encoding='utf-8') as f:
            tokenized = [word_tokenize(trim(tweet[-1])) for tweet in csv.reader(f, delimiter='\t')]
            writer.writerowห(tokenized)
    """
    # get file
    file_random = '/Users/Nozomi/files/processed/random{}.tsv'.format(month, month)
    file_nok = '/Users/Nozomi/files/processed/nok{}.tsv'.format(month, month)
    save_file = open('/Users/Nozomi/files/processed/combined{}.txt'.format(month, month), 'w', encoding='utf-8')
    writer = csv.writer(save_file, delimiter=' ', lineterminator='\n')


    with open(file_nok, 'r', encoding='utf-8') as f:
        lines = csv.reader(f, delimiter='\t')
        writer.writerows(lines)

    with open(file_random, 'r', encoding='utf-8') as f:
        lines = csv.reader(f, delimiter='\t')
        writer.writerows(lines)

    save_file.close()
    
def tokenize_test(file):  # 2012-2-15
    f = open(file, 'r', encoding='utf-8')
    for i, tweet in enumerate(csv.reader(f, delimiter='\t')):
        print(i+1, tweet[0])
        word_tokenize(trim(tweet[-1]))
    f.close()


def make_model(month, skipgram=0, epoch=2):
    file = open('/Users/Nozomi/files/processed/combined{}.txt'.format(month, month), 'r', encoding='utf-8')
    sentences = word2vec.LineSentence(file)
      # CBOW: sg=0, skip-gram: sg=1
    if skipgram == 0:
        model = word2vec.Word2Vec(sentences, sg=skipgram, size=300, min_count=5, window=10, iter=epoch)
        model.wv.save_word2vec_format('/Users/Nozomi/files/processed/{}.bin'.format(month, month), binary=True)
    elif skipgram == 1:
        model = word2vec.Word2Vec(sentences, sg=skipgram, size=300, min_count=5, window=5, iter=epoch)
        model.wv.save_word2vec_format('/Users/Nozomi/files/processed/{}sg.bin'.format(month, month), binary=True)

    file.close()


month2013 = ['2013-%s' % i for i in range(5, 13)]
month2014 = ['2014-%s' % i for i in range(1, 13)]
month2015 = ['2015-%s' % i for i in range(1, 13)]
month2016 = ['2016-%s' % i for i in range(1, 13)]
month2017 = ['2017-%s' % i for i in range(1, 13)]
month2018 = ['2018-%s' % i for i in range(1, 13)]

months = month2014 + month2015 + month2016 + month2017 + month2018

# calculate the cosine similarity of 'nok' and word, and plot the transition
def change(word1, word2='นก'):
    x, y = [], []
    for month in months:
        model = KeyedVectors.load_word2vec_format('/Users/Nozomi/files/processed/{}.bin'.format(month, month), binary=True)
        if month.endswith('-1'):
            x.append(month)
        else:
            x.append(month.split('-')[-1])
        y.append(cos_sim(model.wv[word1], model.wv[word2]))
    for i in y:
        print(i)
    plt.plot(np.arange(0, len(x)), y,'-o')
    plt.xticks(np.arange(0, len(x)), x, rotation='vertical')
    plt.ylabel('cosine similarity')
    plt.ylim(-0.1, 0.8)
    plt.title('Cosine Similarity of {} and {}'.format(word1, word2))
    plt.show()
    
    
# print most similar word of each month
def most():
    for month in months:
        most_month(month)

def most_month(month, k=5):
    model = KeyedVectors.load_word2vec_format('/Users/Nozomi/files/processed/{}.bin'.format(month, month), binary=True)
    results = model.wv.most_similar(positive=['นก'], topn=100)
    i = 0
    # print('\n%s' % month)
    new_list = []
    for result in results:
        if result[0][0].isdigit() == False and result[0][0] not in '#FT!?ๆ.:;”"=\\':
            new_list.append((result[0] + ',' + str(round(result[1], 4))))
            i += 1
        if i == k:
            break
    print(new_list)
    
def cos_sim(v1, v2):
    return round(float(np.dot(v1, v2)) / (norm(v1) * norm(v2)), 4)

def norm(vector):
    return round(np.linalg.norm(vector), 4)


