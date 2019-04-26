from . import db_adaptor
from . import pd_func
from . import support


def get_from_primary(primary_domain):
    """
    Функция возвращает датафрейм со словосочетаниями
    """
    primary_domain_name = get_pretty_domain_name(primary_domain)
    query_list = db_adaptor.primary_select_collocations(primary_domain_name)
    
    if query_list is None:
        return None

    df = pd_func.query_to_df(query_list)
    dict_for_graphic = pd_func.output_for_page(df)
    return dict_for_graphic


def get_from_journal(journal_name):
    """
    Функция возвращает датафрейм со словосочетаниями
    """
    journal_name = get_pretty_domain_name(journal_domain)
    query_list = db_adaptor.journal_select_collocations(journal_name)
    
    if query_list is None:
        return None

    df = pd_func.query_to_df(query_list)  # форма для форкаста
    dict_for_graphic = pd_func.output_for_page(df)
    return dict_for_graphic

def get_pretty_domain_name(domain_name):
    """
    Функция преобразует строку из health_life в Health Life
    """
    words = domain_name.split('_')
    out = []
    for word in words:
        if word == 'and':
            out.append(word)
            continue
        out.append(word.capitalize())
    print(' '.join(out))
    return ' '.join(out)
