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

### Types of lecical innovation (1981 Sornig)
  1. new word for new concept
        > e.g. _smartphone_
  2. new competitive word
        > e.g. _ya_ vs. _you_
  3. new meaning for existing word
        > e.g. _star_ "celebrity"
  4. meaning shift
        > e.g. _gay_ "joyful" -> "homosexual man"

The case of _nók_ is (3) **new meaning for existing word**
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
|2018 | 891,636 | 4,718,447 |
| **total** | **4,156,466** | **22,720,472**|

- collected tweets every 10 minutes in order to prevent from being biased (6 * 24 = 144 points a day)
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

#### Syntactic Structures of Thai

||||
|:-:|:-:|:-:|
|S Verb| S Adj | S **COPULA** Noun |
|S NEG Verb|S NEG Adj| S NEG **COPULA** Noun |
|S AUX Verb|S AUX Adj| S AUX **COPULA** Noun |

copula word (pen เป็น or châi ใช่ “be”) is necessary only when it is nominal sentence

e.g.
- **mâi** (NEG) _nók_ -> the _nók_ is **VERB** 
- **pen** (copula) _nók_ -> the _nók_ is **NOUN**

In these cases, we can presume its Part-of-speech from the collocations.

-> **bigrams may help**

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
- CBoW algorithm (Naili et al, (2017) reported CBoW works better than skip-gram in case of high-frequency word)
- Actually, the result of skip-gram is almost the same
- window size of 5
- 300 dimensional vector
- iterated 3 epochs (loss did not decrease more)

## Results

### [Raw Result (Google Spreadsheet)](https://docs.google.com/spreadsheets/d/13pWKNKzvn0-Fo3icXgtyXuTSDekcZstsReJ82wOvSqE/edit?usp=sharing)

### Population
The total number of tweeter of _nók_
![image](https://user-images.githubusercontent.com/44984892/65207437-cd52b580-dabb-11e9-855a-eedaa091a33a.png)

### 0. Word Frequency

- preliminaly test for general word
- _nók_

**Preliminaly Test**: word frequencies of general words below

|word|phonemic|gloss|grammatical|
|:-:|:-:|:-:|:-:|
|ไม่ |/mâi/|not|negator|
|เป็น|/pen/|be|copula|
|ทำ|/tham/|do|-|

![wf_1](https://user-images.githubusercontent.com/44984892/64902403-bb929c00-d6d0-11e9-9b2a-07fae520c230.png)

There is no abrupt change in word frequencies of general words, it indicates that data is not biased.

While, the word frequency of _nók_ is as below

![wf_2](https://user-images.githubusercontent.com/44984892/64903041-3b723380-d6dc-11e9-9dea-9fc6958910ee.png)
![wf_3](https://user-images.githubusercontent.com/44984892/64903032-1da4ce80-d6dc-11e9-8078-721eb277164a.png)

It bursts in early 2016 and exponentially decays (it is linear in log scale)

### 1. Conditional Probability of Bigram

#### 1-1. preceeding word

|word|phonemic|gloss|grammatical|
|:-:|:-:|:-:|:-:|
|ไม่ |/mâi/|not|negator|
|จะ|/cà/|will|auxiliary verb|
|อย่า|/jàa/|don't|auxiliary verb|
|ความ|/khwaam/|-| nominalizer|

![ppre](https://user-images.githubusercontent.com/44984892/64903016-e8987c00-d6db-11e9-904d-47d80a56892e.png)

#### 1-2. following word

|word|phonemic|gloss|grammatical|
|:-:|:-:|:-:|:-:|
|แล้ว|/lɛ́ɛw/|already|perfect tense|
|อีก|/ìik/|again|-|
|ตลอด|/talɔ̀ɔt/|always|-|

![pfol](https://user-images.githubusercontent.com/44984892/64903588-0cf95600-d6e6-11e9-81b9-2c3fef02b1cd.png)

### 2. PMI at Tweet Level

![pmi](https://user-images.githubusercontent.com/44984892/64903606-606ba400-d6e6-11e9-968a-a8c62030ce32.png)

### 3. Word Embeddings

**Synonyms**

|word|phonemic|gloss|
|:-:|:-:|:-:|
|พลาด| plâat | to miss, to fail |
|เสียใจ | sǐacai | (to feel) sad |
|ผิดหวัง | phìtwǎng | to be disappointed |

similarity rises in late 2015, and become stable (like S-cureve)

![w2v_1](https://user-images.githubusercontent.com/44984892/64904189-86964180-d6f0-11e9-8677-85b906e33052.png)

**Unrelated words**

|word|phonemic|gloss|
|:-:|:-:|:-:|
|โรงเรียน| roongriang | school|
|สยาม| sayǎam | a name of city |
|อาบ |àap | to take a shower | 

similarity does not rise

![w2v_2](https://user-images.githubusercontent.com/44984892/64904134-a5480880-d6ef-11e9-9b1c-2ff74ed2fb5d.png)

"to take a shower" rises a little probably because _nók_ begins to share the same PoS = VERB (distributions are similar)

## Discussion

- The word frequency is decreasing, but all of the three probabilistic measures become stable
- It seems that word frequency shows just “Hit Phenomenon” (Ishi, 2012)
- Even though the frequency of innovative usage is decreasing, but the “proportion” of  innovative usage does not decrease

>**The lexical innovation has already established in the linguistic system of Twitter space**

**limitation**

- Innovation is established in “linguistic system”, but the result did not mention any sociolinguistic factors
- Not “how it diffuses”, but “whether diffused or not”
- We cannot know total acceptance rate
- For morphosyntactically identical polyseme (e.g. noun & noun), syntactic structure does not help
- Tokenizer cannot deal with new lexical entries
- There is no robust PoS-tagger for Thai

### Comparing three measures

||advantage|disadvantage|
|:-:|:-:|:-:|
|conditional probability | needs only tweets that contain the target word |depends on syntactic structure, data A is unavailable to another word|
|tweet level PMI | - | depends on syntactic structure, requires big data (data B)|
|word embeddings | it shows meaning more directly | requires big data (data B) |

### Serendipity

![bat](https://user-images.githubusercontent.com/44984892/64904318-78e1bb80-d6f2-11e9-89c7-233e9e2dc123.png)

at the beginning, _nók_ is mainly used in a sense of love

- e.g. _nók ìik_ : “flirted but failed again”

after that, meaning is gradually broadened to “miss"

- e.g. _nók bàt_ : "miss the ticket"

## Other Examples of Innovation

**ลำไย/lamyai/ and รำคาญ/ramkhaan/**

![lamyai](https://user-images.githubusercontent.com/44984892/64915388-ca8c5380-d78f-11e9-9d97-0570192f908d.png)

