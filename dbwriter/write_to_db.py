import os
import pickle
import itertools
import time
from multiprocessing import Pool

from dbwriter import connect

QUARTERS = itertools.cycle(('Q1', 'Q2', 'Q3', 'Q4'))

def get_quarter(date):
    """
    Возвращает в каком квартале выпущена статья
    """
    if int(date[:2]) < 4:
        return 'Q1'
    if int(date[:2]) < 7:
        return 'Q2'
    if int(date[:2]) < 10:
        return 'Q3'
    return 'Q4'


def is_year_journal(articles):
    for article in articles[:200]:
        if article['publication date'][:2] != '01':
            return False
    return True


def domains_writer(cur, writen_dict):
    """
    Запись всех доменнов журналаб возвращает id записанных или уже существующих поддоменов, указанных в журнале
    """
    # Запись супердомена
    cur.execute("SELECT id FROM primary_domains WHERE name = %s" , (writen_dict['primary'], ))  # запрос id супердомена
    ident = cur.fetchone()
    if ident is None:  # Если нет супердомена
        cur.execute("INSERT INTO primary_domains (name) VALUES (%s) RETURNING id", (writen_dict['primary'],))  # запись в БД
        ident = cur.fetchone()
    primary_id = ident[0]

    # запись домена
    cur.execute("SELECT id FROM domains WHERE name = %s", (writen_dict['domain'],))  # запрос id домена
    ident = cur.fetchone()
    if ident is None:  # если нет домена
        cur.execute("INSERT INTO domains (name, primary_id) VALUES (%s, %s) RETURNING id", (writen_dict['domain'], primary_id))  # запись в бд название домена и id супердомена родителя
        ident = cur.fetchone()
    domain_id = ident[0]
    
    # Проход по поддоменам. Их может быть несколько в одном журнале
    subdomains_id = []

    if type(writen_dict['subdomain']) == str:
        cur.execute("SELECT id FROM subdomains WHERE name = %s", (writen_dict['subdomain'],))
        ident = cur.fetchone()
        if ident is None:  # если нет домена
            cur.execute("INSERT INTO subdomains (name, domain_id) VALUES (%s, %s) RETURNING id", (writen_dict['subdomain'], domain_id))  # запись в бд название поддомена и id домена родителя
            ident = cur.fetchone()
        subdomains_id.append(ident[0])
        return subdomains_id

    for subdomain in set(writen_dict['subdomain']):
        cur.execute("SELECT id FROM subdomains WHERE name = %s", (subdomain,))
        ident = cur.fetchone()
        if ident is None:  # если нет домена
            cur.execute("INSERT INTO subdomains (name, domain_id) VALUES (%s, %s) RETURNING id", (subdomain, domain_id))  # запись в бд название поддомена и id домена родителя
            ident = cur.fetchone()
        subdomains_id.append(ident[0])

    return subdomains_id

def journal_writer(cur, journal_name):
    """
    Функция записи журнала, возвращает id записанного или уже существующего журнала
    """
    cur.execute("SELECT id FROM journals WHERE name = %s", (journal_name,))
    if cur.fetchone() is None:  # если нет журнала
        cur.execute("INSERT INTO journals (name) VALUES (%s) RETURNING id", (journal_name,))  # запись в бд название журнала
        return cur.fetchone()[0]
    return None

def article_writer(cur, article, journal_id):
    """
    Функция записи статьи возвращает id статьи
    """
    
    # запись статьи
    cur.execute("SELECT id FROM years WHERE year = %s", (article['year'],))  # получение id года публикации
    year_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM quarters WHERE name = %s;", (article['quarter'],))  # получение id квартала публикации
    quarter_id = cur.fetchone()[0]
    cur.execute("""INSERT INTO articles (name, doi, abstract, keywords, pub_year_id, pub_quarter_id, journal_id) VALUES
                     (%s, %s, %s, %s, %s, %s, %s) RETURNING id""", (article['article name'], article['doi'], article['abstract'], article.get('keywords', None), year_id, quarter_id, journal_id))

    return cur.fetchone()[0]

def collocations_writer(cur, bigrams: list, trigrams: list):
    """
    Функция записи словосочетаний возвращает список id словосочетаний
    """
    collocations_id = []
    grams = list(set(trigrams+bigrams))  # объеденение списков
    cur.execute("SELECT id, collocation FROM collocations WHERE collocation = ANY (%s)", (grams,))  # Запрос уже существующих словосочетаний
    print(grams)
    exist_grams_query = cur.fetchall()
    exist_grams = []
    # Обработка запроса
    for gram_query in exist_grams_query:
        collocations_id.append(gram_query[0])
        exist_grams.append(gram_query[1])
    # print(exist_grams)
    not_exist_grams = [grams[i] for i in range(0, len(grams)) if  grams[i] not in exist_grams]  # выявление новых словосочетаний
    # print(not_exist_grams)
    if not_exist_grams:  # Если новые словосочетания присутствуют
        query_str = get_query_str(not_exist_grams, bigrams, trigrams)  # состовляем запрос
        cur.execute(query_str)
        for ident in cur:
            collocations_id.append(ident[0])  # получаем индетификаторы словосочетаний
    return collocations_id

def get_query_str(col_list: list, bigrams: list, trigrams: list) -> str:
    """
    Функция для создания строки для внесения данных одним запросом
    для словосочетаний
    """
    indent = "  "
    query_list = []
    # Состовление списка кортежей, в кортеже 1-ое значение - словосочетание
    # Второе - ссылочный ключ на тип
    for gram in col_list:
        if gram in trigrams:
            query_list.append((gram, 2))
        else:
            query_list.append((gram, 1))
    # Состовление запроса
    query_str = "INSERT INTO collocations (collocation, col_type_id) VALUES"
    # print(query_list)
    for collocation in query_list[:-1]:
        input_str = "($$%s$$, %s)" % (collocation[0], collocation[1])
        query_str += "\n" + indent + input_str +","
    query_str += "\n" + ("($$%s$$, %s)" % (query_list[-1][0], query_list[-1][1]))+" RETURNING id" # Последняя строка должна содержать возврат id
    return query_str


def articles_collocations_writer(cur, article_id, collocations_id):
    """
    Функция записи взаимосвязей между статьей и словосочетаниями
    """
    query_str = "INSERT INTO articles_collocations (article_id, collocation_id) VALUES"
    ident = "  "
    for collocation_id in collocations_id[:-1]:
        query_str += "\n" + ident + f'({article_id}, {collocation_id})' + ","
    
    query_str += "\n" + ident + f'({article_id}, {collocations_id[-1]})'
    cur.execute(query_str)



def read_pickle(file_path):
    """
    Десериализация файла
    """
    with open(file_path, 'rb') as file:
        writen_dict = pickle.load(file)
    return writen_dict

def write_to_db(file_path, cur, connector):
    """
    Запись в БД
    """
    # запись журнала

    writen_dict = read_pickle(file_path)
    subdomains_id = domains_writer(cur, writen_dict)


    journal_id = journal_writer(cur, writen_dict['journal name'])
    if journal_id is None:
        # print(f"Journal: {writen_dict['journal name']} is already exist")
        return True
    print(f"Processing Journal: {writen_dict['journal name']} wait")
    # матрица отношения сабдоменов и журналов
    for subdomain_id in subdomains_id:
        print('subdomain: ' , subdomain_id, '  journal:  ', journal_id)
        cur.execute("INSERT INTO subdomains_journals (subdomain_id, journal_id) VALUES (%s, %s)", (subdomain_id, journal_id))  # создание связи
   
    is_year_pub = is_year_journal(writen_dict['articles'])
    print(len(writen_dict['articles']))
    for article in writen_dict['articles']:

        # подготовка даты к записи
        if is_year_pub:
            article['quarter'] = next(QUARTERS) 
        else:
            article['quarter'] = get_quarter(article['publication date'])
        article['year'] = int(article['publication date'][3:])  # определеняем год выпуск
        article_id = article_writer(cur, article, journal_id)  # запись статьи
        if article['trigrams'] or article['bigrams']:
            collocations_id = collocations_writer(cur, article['bigrams'], article['trigrams'])  # запись словосочетаний статьи
            articles_collocations_writer(cur, article_id, collocations_id)  # запись связи между словосочетаниями и статьей
        print('Article writen:  ', article['doi'])
    print(f"Journal: {writen_dict['journal name']} writen")



def main():
   
    walking_path = os.path.join(os.getcwd(), 'pkl')
    print('START')
    file_list = []
    i = 0
    for root, _, files in os.walk(walking_path):
        if not files:
            continue
        for file in files:
            file_list.append(file)
            file_path = os.path.join(os.getcwd(), root, file)
            # print('Path:    ', file_path)
            (cur, connector) = connect.connect_to_db()
            write_to_db(file_path, cur, connector)
            connect.commit(cur, connector)
    print(len(set(file_list)))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
