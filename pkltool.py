#!/usr/bin/env python3

# -*- coding:utf-8 -*-


import pickle
import re
import pandas as pd


PKL_FILE_PATH = """/home/user035/my-files/Yandex.Disk/projects/scienceforecast\
/pkl/Physical Sciences and Engineering/Chemical Engineering/Bioengineering/\
ActaBiomaterialia.pkl"""


def create_top_journal_list_by_year(year):

    filtered_articles_list = []
    bigrams_list = []
    trigrams_list = []

    with open(PKL_FILE_PATH, 'rb') as file:
        data = pickle.load(file)

    for article in data['articles']:
        result = re.match(r'^(\d\d).*(\d\d\d\d)', article['publication date'])
        if result[2] in year:
            filtered_articles_list.append(article)
            bigrams_list.append(article['bigrams'])
            trigrams_list.append(article['trigrams'])

    # Flatten bigram and trigrams lists
    flat_bigrams_list = [item for sublist in bigrams_list for item in sublist]
    flat_trigrams_list = [item
                          for sublist in trigrams_list for item in sublist]

    # Clean linguistic bugs
    flat_bigrams_list = [x for x in flat_bigrams_list if "’ s" not in x]

    # Create lists with unique set of collocations. Need to calculate number of
    # each found collocation
    bigrams_uniq_list = set(flat_bigrams_list)
    trigrams_uniq_list = set(flat_trigrams_list)

    # Lists of collocation lists ([collocation, number])
    bigrams_counted = []
    trigrams_counted = []

    for bigram in bigrams_uniq_list:
        bigrams_counted.append([bigram, flat_bigrams_list.count(bigram)])

    for trigram in trigrams_uniq_list:
        trigrams_counted.append([trigram, flat_trigrams_list.count(trigram)])

    bigrams_frame = pd.DataFrame(bigrams_counted)
    trigrams_frame = pd.DataFrame(trigrams_counted)

    frames = bigrams_frame.nlargest(5, 1).append(trigrams_frame.nlargest(5, 1))

    frames['year'] = year
    frames.columns = ['collocation', 'number', 'year']

    return frames

    # result.to_excel(f"{year}.xlsx", sheet_name='Sheet_name_1')
    # print(result)


def normalize_range_data_frame(frame):
    """
    Functions gets a frame of sevaral years of type collocation, number, year.
    Adds to this frame zero number of collocations in year records when they
    were absent (Example: matrix ECM 0 2015, matrix ECM 0 2016)
    """
    collocations = frame['collocation'].unique()
    years = frame['year'].unique()

    for year in years:
        for collocation in collocations:
            test_frame = frame[(frame['year'] == year) &
                               (frame['collocation'] == collocation)]
            if test_frame.empty:
                frame = frame.append({'collocation': collocation, 'number': 0,
                                      'year': year}, ignore_index=True)

    return frame


def get_top_ten_from_frame(frame):

    collocations = frame['collocation'].unique()

    for collocation in collocations:
        col_frame = frame[collocation]
        print('---')
        print(col_frame)

if __name__ == '__main__':

    words_2015 = create_top_journal_list_by_year('2015')
    words_2016 = create_top_journal_list_by_year('2016')
    words_2017 = create_top_journal_list_by_year('2017')
    words_2018 = create_top_journal_list_by_year('2018')


    result_frame = pd.concat([words_2015, words_2016, words_2017, words_2018])

    # result_frame.to_excel("output.xlsx", sheet_name='Sheet_name_1')

    normalized_frame = normalize_range_data_frame(result_frame).sort_values(
        by=['collocation', 'year'])

    get_top_ten_from_frame(normalized_frame)


