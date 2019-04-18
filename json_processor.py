#!/usr/bin/env python3

# -*- coding:utf-8 -*-

import os
import json
import pickle

import collocator

SRC_PATH = 'journals'


def process_json(file_path_string):
    """
    Main function processing json file to pkl or db.
    TODO: Change to file dir or complex params.
    """
    print('Processing: ' + file_path_string)
    journals_dict = get_journal_data_from_json(file_path_string)
    journal_data_with_cols_dict = get_collocations_info(journals_dict)
    write_pkl(journal_data_with_cols_dict)


def get_journal_data_from_json(file_path_string):
    """
    Returns journal's dictionary from JSON object.
    """
    with open(file_path_string) as fp:
        data = json.load(fp)

    return data


def get_collocations_info(journal_data_dict):
    """
    Appends collocations to journal's data dictionary.
    """
    for article in journal_data_dict['articles']:
        article['bigrams'] = collocator.get_bigrams(article['abstract'])
        article['trigrams'] = collocator.get_trigrams(
            article['abstract'])

    journal_data_with_cols_dict = journal_data_dict

    return journal_data_with_cols_dict


def write_pkl(journal_data):
    """
    Serializes journal_data_to pkl file in 'pkl' dir
    """
    primary_domain = journal_data['primary']
    domain = journal_data['domain']
    subdomain = journal_data['subdomain']

    file_name = journal_data['journal name'].replace(' ', '') + '.pkl'

    run_path = os.path.dirname(os.path.abspath(__file__))

    pkl_dir = os.path.join(run_path, 'pkl', primary_domain, domain,
                           subdomain[0])
    print(pkl_dir)
    pkl_file_path = os.path.join(run_path, 'pkl', primary_domain, domain,
                                 subdomain[0], file_name)
    print(pkl_file_path)

    if not os.path.exists(pkl_dir):
        os.makedirs(pkl_dir)

    if not os.path.exists(pkl_file_path):

        print('Writing file: ' + pkl_file_path)

        with open(pkl_file_path, 'wb') as file:
            pickle.dump(journal_data, file)

        print('File: ' + pkl_file_path + ' written')


def write_to_db():
    """
    TODO. Function to write journal data to database. For example, PostgreSQL.
    """
    pass


for root, subdirs, files in os.walk(SRC_PATH):

    for file in files:
        if file.endswith(".json"):
            existing_json_file = os.path.join(root, file)
            # json_splitted_abs_path = existing_json_file.split(os.sep)
            process_json(existing_json_file)


# src_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src',
#                         'Catalysis', 'AppliedCatalysisB:Environmental.json')
# process_json(src_file)
