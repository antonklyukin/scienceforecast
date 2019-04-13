#!/usr/bin/env python3

# -*- coding:utf-8 -*-

import nltk
import string


def get_lemmas_from_text(text):
    tokens_dict = nltk.word_tokenize(text)
    wn_lemmatizer = nltk.WordNetLemmatizer()
    lemmas_dict = [wn_lemmatizer.lemmatize(token) for token in tokens_dict]
    return lemmas_dict


def clear_lemmas_dict(lemmas):
    stop_punct = list(string.punctuation)
    custom_punct = ['“', '”']
    # stop_words = nltk.corpus.stopwords.words('english')
    stop = stop_punct + custom_punct
    cleared_lemmas_dict = [lemma for lemma in lemmas if lemma not in stop]
    return cleared_lemmas_dict


def get_bigrams(lemmas):
    text_lemmas_dict = get_lemmas_from_text(lemmas)
    cleared_dict = clear_lemmas_dict(text_lemmas_dict)
    possed_lemmas_dict = nltk.pos_tag(cleared_dict)
    bigram_finder = nltk.collocations.BigramCollocationFinder.from_words(
        possed_lemmas_dict)
    bigram_finder.apply_ngram_filter(b_filter)
    bigrams_list = []
    for k, v in bigram_finder.ngram_fd.items():
        bigrams_list.append(str(k[0][0]) + " " + str(k[1][0]))
    return bigrams_list


def b_filter(pair1, pair2):
    (w1, t1), (w2, t2) = pair1, pair2
    condition_1 = (t1 == 'NNP') and (t2 == 'NN')
    condition_2 = (t1 == 'NN') and (t2 == 'NNP')
    # condition_3 = (t1 == 'JJ') and (t2 == 'NN')
    return not (condition_1 or condition_2)


def get_trigrams(lemmas):
    text_lemmas_dict = get_lemmas_from_text(lemmas)
    cleared_dict = clear_lemmas_dict(text_lemmas_dict)
    possed_lemmas_dict = nltk.pos_tag(cleared_dict)
    trigram_finder = nltk.collocations.TrigramCollocationFinder.from_words(
        possed_lemmas_dict)
    trigram_finder.apply_ngram_filter(t_filter)
    trigrams_list = []
    for k, v in trigram_finder.ngram_fd.items():
        trigrams_list.append(str(k[0][0]) + " " + str(k[1][0]) + " " +
                             str(k[2][0]))
    return trigrams_list


def t_filter(pair1, pair2, pair3):
    (w1, t1), (w2, t2), (w3, t3) = pair1, pair2, pair3
    condition_1 = (t1 == 'JJ') and (t2 == 'CC') and (t3 == 'NN')
    condition_2 = (t1 == 'JJ') and (t2 == 'JJ') and (t3 == 'NN')
    condition_3 = (t1 == 'JJ') and (t2 == 'NN') and (t3 == 'NN')
    return not (condition_1 or condition_2 or condition_3)
