import psycopg2

from .settings import DB_SETTINGS

def primary_select_collocations(name):
    connector= psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("""SELECT collocations.collocation, years.year, quarters.name FROM articles_collocations
                     JOIN collocations ON (collocations.id = articles_collocations.collocation_id)
                     JOIN articles ON (articles.id = articles_collocations.article_id)
                     JOIN years ON (years.id = articles.pub_year_id)
                     JOIN quarters ON (quarters.id = articles.pub_quarter_id)
                     WHERE articles_collocations.article_id IN (
                     SELECT id
                     FROM articles
                     WHERE journal_id IN (
                       SELECT id FROM journals WHERE id IN (
                         SELECT subdomain_id FROM subdomains_journals WHERE subdomain_id IN (
                           SELECT id FROM subdomains WHERE domain_id IN (
                             SELECT id from domains WHERE primary_id = (
                               SELECT id from primary_domains WHERE name = %s)
                              )
                           )
                         )
                       )
                     )
                """, (name, ))


    output_query = cur.fetchall()
    cur.close()
    connector.close()
    if not output_query:
        return None
    output = []
    for row in output_query:
        output.append(row)

    return output


def domain_select_collocations(name):
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("""SELECT collocations.collocation, years.year, quarters.name FROM articles_collocations
                     JOIN collocations ON (collocations.id = articles_collocations.collocation_id)
                     JOIN articles ON (articles.id = articles_collocations.article_id)
                     JOIN years ON (years.id = articles.pub_year_id)
                     JOIN quarters ON (quarters.id = articles.pub_quarter_id)
                     WHERE articles_collocations.article_id IN (
                     SELECT id
                     FROM articles
                     WHERE journal_id IN (
                       SELECT id FROM journals WHERE id IN (
                         SELECT subdomain_id FROM subdomains_journals WHERE subdomain_id IN (
                           SELECT id FROM subdomains WHERE domain_id IN (
                             SELECT id from domains WHERE name = %s)
                           )
                         )
                       )
                     )
                """, (name, ))
    
    output_query = cur.fetchall()
    cur.close()
    connector.close()
    if not output_query:
        return None
    output = []
    for row in output_query:
        output.append(row)

    return output


def subdomain_select_collocations(name):
    connector= psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("""SELECT collocations.collocation, years.year, quarters.name FROM articles_collocations
                     JOIN collocations ON (collocations.id = articles_collocations.collocation_id)
                     JOIN articles ON (articles.id = articles_collocations.article_id)
                     JOIN years ON (years.id = articles.pub_year_id)
                     JOIN quarters ON (quarters.id = articles.pub_quarter_id)
                     WHERE articles_collocations.article_id IN (
                     SELECT id
                     FROM articles
                     WHERE journal_id IN (
                       SELECT id FROM journals WHERE id IN (
                         SELECT subdomain_id FROM subdomains_journals WHERE subdomain_id IN (
                           SELECT id FROM subdomains WHERE name = %s)
                         )
                       )
                     )
                """, (name, ))
    
    output_query = cur.fetchall()
    cur.close()
    connector.close()
    if not output_query:
        return None
    output = []
    for row in output_query:
        output.append(row)

    return output


def get_list_of_journals_in_subdomain(subdomain_name):
    """
    Функция берет нормализированное (astronomy_and_astrophysics) название
    поддомена и выдает dict({name: "Absolute Radiometry", id: "124"}, ...)
    """
    pass


def get_list_of_subdomains_in_domain(domain_name):
    """
    Функция берет нормализированное (physics_and_astronomy) название домена
    и выдает dict({name: "Astronomy and Astrophysics", 
    link_name: "astronomy_and_astrophysics"}, ...)
    """
    pass


def get_journal_collocations_yearly_data(journal_id, start_year=None,
                                         end_year=None ):
    """
    Функция берет id журнала (124), год начала снятия данных(если указан)
    и год конца снятия данных (если указан) и выдает dict() с погодичными
    данными для дальнейшей обработки??? для построения графика
    collocation  number  year
    DNA damage       0  2010
    DNA damage      35  2011
    DNA damage      29  2012
    DNA damage      26  2013
    T cell      35  2010
    T cell      26  2011
    T cell      40  2012
    T cell      33  2013
    """
    pass


def get_total_list_of_domains():
    """
    возвращает список всех доменов
    """
    pass


def get_total_list_of_subdomains():
    """
    возвращает список всех поддоменов
    """
    pass