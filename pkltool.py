#!/usr/bin/env python3

# -*- coding:utf-8 -*-


import joblib
import re
import pandas as pd
import os


run_path = os.path.dirname(os.path.abspath(__file__))

PKL_FILE_PATH = os.path.join(run_path, 'pkl', 'Life Sciences/Biochemistry, Genetics and Molecular Biology/Cancer\
 Research/BiochemicalandBiophysicalResearchCommunications.pkl')


# PKL_FILE_PATH = '/home/antony/my-files/Yandex.Disk/projects/scienceforecast\
# /pkl/Life Sciences/Biochemistry, Genetics and Molecular Biology/Cancer\
#  Research/BiochemicalandBiophysicalResearchCommunications.pkl'


def create_top_journal_list_by_year(year):

    filtered_articles_list = []
    bigrams_list = []
    trigrams_list = []

    with open(PKL_FILE_PATH, 'rb') as file:
        data = joblib.load(file)

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
    frames.reset_index(inplace=True)
    frames['year'] = year
    del frames['index']
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


def get_top_from_frame(frame, number_of_collocations=7):

    number_of_years_in_frame = len(frame['year'].unique())

    uniq_collocations_in_frame = frame['collocation'].unique()

    if (len(uniq_collocations_in_frame) > number_of_collocations):
        drop_rare_collocations(frame)

    return frame


def drop_rare_collocations(frame, number_of_collocations=7):
    number_of_years_in_frame = len(frame['year'].unique())
    uniq_collocations_in_frame = frame['collocation'].unique()
    number_of_uniq_collocations = len(uniq_collocations_in_frame)
    zero_num = number_of_years_in_frame - 1
    while (number_of_uniq_collocations > number_of_collocations) and (zero_num != 0):
        for collocation in uniq_collocations_in_frame:
            slice_frame = frame[frame['collocation'] == collocation]
            if number_of_uniq_collocations == number_of_collocations:
                break
            if (len(slice_frame[slice_frame['number'] == 0]) == zero_num):
                # print(slice_frame)
                frame.drop(frame.loc[frame['collocation'] == collocation].index, inplace=True)
            uniq_collocations_in_frame = frame['collocation'].unique()
            number_of_uniq_collocations = len(uniq_collocations_in_frame)
        zero_num -= 1

    return frame


year_list = []
for year in range(2010, 2014):
    year_list.append(create_top_journal_list_by_year(f'{year}'))


result_frame = pd.concat(year_list)


normalized_frame = normalize_range_data_frame(result_frame).sort_values(
        by=['collocation', 'year'])


print(drop_rare_collocations(normalized_frame, 7))

