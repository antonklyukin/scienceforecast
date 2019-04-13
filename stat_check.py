#!/usr/bin/env python3

# -*- coding:utf-8 -*-

import json
import os.path
import pickle
import pandas as pd
import matplotlib as plt


import collocator




# journal_file = open(os.path.dirname(__file__) + '
# /src/BiotechnologyAdvances.json')


# with open(os.path.dirname(__file__) + 'src/Biomaterials.json') as fp:
#     data = json.load(fp)

# articles = data['articles']


# if not os.path.isfile('./Biomaterials.pkl'):

#     for article in data['articles']:
#         article["bigrams"] = collocator.get_bigrams(article['abstract'])
#         article["trigrams"] = collocator.get_trigrams(
#             article['abstract'])

#     with open('Biomaterials.pkl', 'wb') as f:
#         pickle.dump(data, f)



bi_collocations = {}
tri_collocations = {}




def get_top_bigrams(article_records):

    for article in article_records:

        for bigram in article['bigrams']:
            if bigram not in bi_collocations:
                bi_collocations[bigram] = 1
            else:
                bi_collocations[bigram] += 1

    print(pd.Series(bi_collocations).nlargest(7))


def get_top_trigrams(article_records):

    for article in article_records:
        for trigram in article['trigrams']:
            if trigram not in tri_collocations:
                tri_collocations[trigram] = 1
            else:
                tri_collocations[trigram] += 1

    print(pd.Series(tri_collocations).nlargest(7))


def get_journal_info(pkl_file):

    data = []

    if os.path.isfile('./' + pkl_file):
        with open(pkl_file, 'rb') as f:
            data = pickle.load(f)

    # Получаем DataFrame с данными статей журнала
    articles_df = pd.DataFrame(data['articles'])

    list_of_issue_dates = articles_df['publication date'].unique()

    list_of_2010 = [issue for issue in list_of_issue_dates if '2010' in issue]

    print(list_of_issue_dates)

    # for issue_date in list_of_2010:
    #     list_of_articles = articles_df.loc[
    #         articles_df['publication date'] == issue_date]
    #     print('*' * 78)
    #     print(issue_date)
    #     print(len(list_of_articles))
    #     print('*' * 78)
    #     print(list_of_articles)

    #     get_top_bigrams(list_of_articles.to_dict('records'))

    #     get_top_trigrams(list_of_articles.to_dict('records'))

    # return journal_file_dict


get_journal_info('Biomaterials.pkl')
