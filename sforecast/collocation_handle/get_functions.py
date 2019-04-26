from . import db_adaptor
from . import pd_func
from . import support

import os
import json


def get_from_primary(primary_domain):
    """
    Функция возвращает датафрейм со словосочетаниями
    """
    primary_domain_name = url_form_to_name(primary_domain)
    query_list = db_adaptor.primary_select_collocations(primary_domain_name)
    
    if query_list is None:
        return None

    df = pd_func.query_to_df(query_list)
    dict_for_graphic = pd_func.output_for_page(df)
    return dict_for_graphic, primary_domain_name


def get_from_journal(journal_id):
    """
    Функция возвращает датафрейм со словосочетаниями
    """

    output = from_journal_for_forecast(journal_id)  # форма для форкаста
    print(output)
    if not output:
        return None
    df = output[0]
    journal_name = output[1]
    dict_for_graphic = pd_func.output_for_page(df)
    return dict_for_graphic, journal_name

def from_journal_for_forecast(journal_id):

    output = db_adaptor.journal_select_collocations(journal_id)
    if not output:
        return None
    query_list = output[0]
    journal_name = output[1]
    return pd_func.query_to_df(query_list), journal_name # форма для форкаста
    

def url_form_to_name(domain_url):
    """
    Функция преобразует url в название согласно файлу
    """
    file_path = os.path.join(os.getcwd(), 'collocation_handle', 'domains.json')
    with open(file_path) as file:
        data = json.load(file)
    for super_domain in data:
        if domain_url == super_domain['url']:
            return super_domain['name']
        for domain in super_domain['domains']:
            if domain_url == domain['url']:
                return domain['name']
            for subdomain in domain['subdomains']:
                if domain_url == subdomain['url']:
                    return subdomain['name']

    return None
