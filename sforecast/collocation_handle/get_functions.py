from . import db_adaptor
from . import pd_func
from . import support


def get_from_primary(primary_domain):
    """
    Функция возвращает датафрейм со словосочетаниями
    """
    primary_domain_name = support.pretty_domain_name(primary_domain)
    query_list = db_adaptor.primary_select_collocations(primary_domain_name)
    
    if query_list is None:
        return None

    df = pd_func.query_to_df(query_list)
    return df

