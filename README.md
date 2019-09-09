# Probabilistic Measures for Diffusion of Innovation: As Seen in the Usage of Verbal “Nok” in Thai Twitter

Proceedings of The 33rd Pacific Asia Conference on Language, Information and Computation - [PACLIC33](https://jaslli.org/paclic33/)
 
## What is this about?
 - A case study about language change in Thai Twitter
 - Target is an innovative usage of _nók_
 - Original meaning is "bird", now it is also used in the meaning "to fail to (flirt)"
 - Its polysemy makes it difficult to analyze diffusion by using only word frequency
 - Then, we adopted 3 probabilistic measures:
   1. Conditional Probability of Bigram
   2. Pointwise Mutual Information at Tweet Level
   3. Diachronic Word Embeddings
   
## Data
- tweets written in Thai
- January 2012 - December 2018 
  - data set A : tweets containing the word nók 1000 - 2500 tweets / day,  total 4,156,466 tweets
  - data set B : random tweets 10000 - 25000 tweets / day,  total 21,558,621 tweets
- collected tweets every 10 minutes in order to prevent from being biased
- tokenizer : [`PyThaNLP 2.0.3`](https://github.com/PyThaiNLP/pythainlp) using Maximum-Matching algorithm (`engine=newmm`)

    ~~~python
    from pythainlp import word_tokenizer
    word_tokenizer('นกอีกแล้วอยากจะตาย')
    
    >>> ['นก', 'อีกแล้ว', 'อยาก', 'จะ', 'ตาย']
    ~~~

## Measures
### 1. Conditional Probability of Bigram
<img src="https://latex.codecogs.com/gif.latex?p_{pre}(w_i|nok)&space;=&space;\frac{C(w_i,~nok)}{\sum_w&space;C(w,~nok)}" title="p_{pre}(w_i|nok) = \frac{C(w_i,~nok)}{\sum_w C(w,~nok)}" />
<img src="https://latex.codecogs.com/gif.latex?p_{fol}(w_i|nok)&space;=&space;\frac{C(nok,~w_i)}{\sum_w&space;C(nok,~w)}" title="p_{fol}(w_i|nok) = \frac{C(nok,~w_i)}{\sum_w C(nok,~w)}" />

- numerator  C(wi, nok) : the number of bigram where the first word is wi and the second word is nók
- denominator  ΣwC(w, nok) : the total number of bigrams that contain nók as the second word (normalization factor)

_pre_, _fol_ are abbreviations of "preceeding" and "following", respectively

### 2. Pointwise Mutual Information at Tweet Level
<img src="https://latex.codecogs.com/gif.latex?{\rm&space;PMI}(w_i,~nok)&space;=&space;\log_2\frac{p(w_i,~nok)}{p(w_i)~p(nok)}" title="{\rm PMI}(w_i,~nok) = \log_2\frac{p(w_i,~nok)}{p(w_i)~p(nok)}" />
<img src="https://latex.codecogs.com/gif.latex?{\rm&space;PMI}(nok,~w_i)&space;=&space;\log_2\frac{p(nok,~w_i)}{p(nok)~p(w_i)}" title="{\rm PMI}(nok,~w_i) = \log_2\frac{p(nok,~w_i)}{p(nok)~p(w_i)}" />

## 3. Diachronic Word Embeddings
cosine similarity of two word embeddings: _nók_ and synonym _s_

<img src="https://latex.codecogs.com/gif.latex?{\rm&space;cos~similarity}(\vec{nok},~\vec{s})&space;=&space;\frac{\vec{nok}\cdot\vec{s}}{\|\vec{nok}\|\|\vec{s}\|}" title="{\rm cos~similarity}(\vec{nok},~\vec{s}) = \frac{\vec{nok}\cdot\vec{s}}{\|\vec{nok}\|\|\vec{s}\|}" />

use [`gensim 3.7.3`](https://radimrehurek.com/gensim/) and made word embeddings of data of each month
 - CBoW algorithm (CBoW works better than skip-gram in case of high-frequency word (Naili et al, 2017))
 - window size of 5
 - 300 dimensional vector
 - iterated 3 epochs (loss did not decrease more)
