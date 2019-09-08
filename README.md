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
<img src="https://latex.codecogs.com/gif.latex?{\rm&space;cos~similarity}(\vec{nok},~\vec{s})&space;=&space;\frac{\vec{nok}\cdot\vec{s}}{\|\vec{nok}\|\|\vec{s}\|}" title="{\rm cos~similarity}(\vec{nok},~\vec{s}) = \frac{\vec{nok}\cdot\vec{s}}{\|\vec{nok}\|\|\vec{s}\|}" />
