# Probabilistic Measures for Diffusion of Innovation: As Seen in the Usage of Verbal “Nok” in Thai Twitter

Proceedings of The 33rd Pacific Asia Conference on Language, Information and Computation - [PACLIC33](https://jaslli.org/paclic33/)
 
## What is this about?
- A case study about a lexical innovation in Thai Twitter
- Target is an innovative verbal usage of _nók_
- The original meaning is "bird", now it is also used in the meaning "to fail to one's expectation"
- especially in a sence of love or flirting
- Word frequency is the popular method for investigating language change, but polysemy of _nók_ makes it difficult to analyze diffusion by using only word frequency
- Then, we adopted 3 probabilistic measures instead:
  1. Conditional Probability of Bigram
  2. Pointwise Mutual Information at Tweet Level
  3. Diachronic Word Embeddings

## Questions
1. What kind of measure is effective for polysemy?
2. How to quantify the progress of diffusion of nok?


## Data and Pre-proessing

tweets written in Thai : January 2012 - December 2018 

|Year | A: Tweets contain _nók_ | B: Random Tweets |
|:-:|--:|--:|
|2012 | 118,799 | 0 |
|2013 | 476,365 | 2,529,665 |
|2014 | 425,421 | 3,732,020 |
|2015 | 395,334 | 3,153,596 |
|2016 | 778,243 | 3,434,185 |
|2017 | 1,070,668 | 5,152,559 |
|2018 | 891,636 | 3,556,596 |
| **total** | **4,156,466** | **21,558,621**|

- collected tweets every 10 minutes in order to prevent from being biased 
- tokenizer : [`PyThaNLP 2.0.3`](https://github.com/PyThaiNLP/pythainlp) using Maximum-Matching algorithm (`engine='newmm'`)

    ~~~python
    from pythainlp import word_tokenizer
    word_tokenizer('นกอีกแล้วอยากจะตาย')
    
    >>> ['นก', 'อีกแล้ว', 'อยาก', 'จะ', 'ตาย']
    ~~~
- Maximum-Matching algorithm requires vocaburary set (dictionary). In this reserach, we removed all compound words that contain the morpheme _nók_ beforehand. (e.g. _nókphirâap_ "pigeon")

    ~~~python
    word_tokenizer('นกพิราบ')
    
    >>> ['นก', 'พิราบ']
    ~~~

## Probabilistic Measures
### 1. Conditional Probability of Bigram
<img src="https://latex.codecogs.com/gif.latex?p_{pre}(w_i|nok)&space;=&space;\frac{C(w_i,~nok)}{\sum_w&space;C(w,~nok)}" title="p_{pre}(w_i|nok) = \frac{C(w_i,~nok)}{\sum_w C(w,~nok)}" />
<img src="https://latex.codecogs.com/gif.latex?p_{fol}(w_i|nok)&space;=&space;\frac{C(nok,~w_i)}{\sum_w&space;C(nok,~w)}" title="p_{fol}(w_i|nok) = \frac{C(nok,~w_i)}{\sum_w C(nok,~w)}" />

- numerator  C(wi, nok) : the number of bigram where the first word is wi and the second word is nók
- denominator  ΣwC(w, nok) : the total number of bigrams that contain nók as the second word (normalization factor)

_pre_, _fol_ are abbreviations of "preceeding" and "following", respectively

example: _nók A B nók B C nók A_ (A,B,C are words)

(*, nók) : (B, nók), (C, nók) ... 2 bigrams

- p<sub>pre</sub>(A|nok) = 0
- p<sub>pre</sub>(B|nok) = 1/2
- p<sub>pre</sub>(C|nok) = 1/2

(nók, *) : (nók, A), (nók, B), (nók, A) ... 3 bigrams

- p<sub>fol</sub>(A|nok) = 2/3
- p<sub>fol</sub>(B|nok) = 1/3
- p<sub>fol</sub>(C|nok) = 0

I was inspired by P<sub>CONTINUATION</sub> of Kneser-Ney Smoothing (but not the same one) 

### 2. Pointwise Mutual Information at Tweet Level
<img src="https://latex.codecogs.com/gif.latex?{\rm&space;PMI}(w_i,~nok)&space;=&space;\log_2\frac{p(w_i,~nok)}{p(w_i)~p(nok)}" title="{\rm PMI}(w_i,~nok) = \log_2\frac{p(w_i,~nok)}{p(w_i)~p(nok)}" />
<img src="https://latex.codecogs.com/gif.latex?{\rm&space;PMI}(nok,~w_i)&space;=&space;\log_2\frac{p(nok,~w_i)}{p(nok)~p(w_i)}" title="{\rm PMI}(nok,~w_i) = \log_2\frac{p(nok,~w_i)}{p(nok)~p(w_i)}" />

- p(w<sub>i</sub>, nok): the probability that one tweet contains the bigram (w<sub>i</sub>, nók) 

- p(w<sub>i</sub>): the probability that one tweet contains the word w<sub>i</sub>

### 3. Diachronic Word Embeddings
cosine similarity of two word embeddings: _nók_ and synonym _s_

<img src="https://latex.codecogs.com/gif.latex?{\rm&space;cos~similarity}(\vec{nok},~\vec{s})&space;=&space;\frac{\vec{nok}\cdot\vec{s}}{\|\vec{nok}\|\|\vec{s}\|}" title="{\rm cos~similarity}(\vec{nok},~\vec{s}) = \frac{\vec{nok}\cdot\vec{s}}{\|\vec{nok}\|\|\vec{s}\|}" />

use [`gensim 3.7.3`](https://radimrehurek.com/gensim/) and made word embeddings of data of each month
- CBoW algorithm (CBoW works better than skip-gram in case of high-frequency word (Naili et al, 2017))
- window size of 5
- 300 dimensional vector
- iterated 3 epochs (loss did not decrease more)

## Results

### [data](https://docs.google.com/spreadsheets/d/13pWKNKzvn0-Fo3icXgtyXuTSDekcZstsReJ82wOvSqE/edit?usp=sharing)

### 0. Word Frequency

- preliminaly test for general word
- _nók_

**Preliminaly Test**: word frequencies of general words below

|word|phonemic|gloss|grammatical|
|:-:|:-:|:-:|:-:|
|ไม่ |/mâi/|not|negator|
|เป็น|/pen/|be|copula|
|ทำ|/tham/|do|-|

There is no abrupt change in word frequencies of general words.

### 1. Conditional Probability of Bigram
#### 1-1. preceeding word

|word|phonemic|gloss|grammatical|
|:-:|:-:|:-:|:-:|
|ไม่ |/mâi/|not|negator|
|จะ|/cà/|will|auxiliary verb|
|อย่า|/jàa/|don't|auxiliary verb|
|ความ|/khwaam/|-| nominalizer|

#### 1-2. following word

|word|phonemic|gloss|grammatical|
|:-:|:-:|:-:|:-:|
|แล้ว|/lɛ́ɛw/|already|perfect tense|
|อีก|/ìik/|again|-|
|ตลอด|/talɔ̀ɔt/|always|-|
|บัตร|/bàt/|ticket|-|

### 2. PMI at Tweet Level

### 3. Word Embeddings

### Serendipity

### Conclusion

