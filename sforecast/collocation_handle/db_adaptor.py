import psycopg2
import json

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


def get_total_list_of_domains(json_file, superdomain_url_name):
    """
    возвращает список всех доменов в требуемом супердомене (разделе) в
    формате [{'Chemical Engineering': 'chemical-engineering'},
    {'Chemistry': 'chemistry'}]
    """
    total_list_of_domains = []
    with open(json_file) as f:
        data = json.load(f)
        for super_domain in data:
            if (super_domain['url'] == superdomain_url_name):
                for domain in super_domain['domains']:
                    total_list_of_domains.append({domain['name']:
                                                  domain['url']})

    return total_list_of_domains


def get_total_list_of_subdomains(json_file, superdomain_url_name,
                                 domain_url_name):
    """
    возвращает список всех поддоменов в требуемом домене в
    формате [{'Chemical Engineering': 'chemical-engineering'},
    {'Chemistry': 'chemistry'}]
    """
    total_list_of_subdomains = []
    with open(json_file) as f:
        data = json.load(f)
        for super_domain in data:
            if (super_domain['url'] == superdomain_url_name):
                for domain in super_domain['domains']:
                    if domain['url'] == domain_url_name:
                        for subdomain in domain['subdomains']:
                            total_list_of_subdomains.append({subdomain['name']:
                                                            subdomain['url']})

    return total_list_of_subdomains


def get_available_list_of_domains():
    """
    возвращает список всех доменов в требуемом супердомене (разделе),
    в которых есть журналы в базе
    формате ['Chemical Engineering', 'Chemistry'}
    """
    pass


def get_available_list_of_subdomains():
    """
    возвращает список всех поддоменов в требуемом домене,
    в которых есть журналы в базе
    формате ['Chemical Engineering', 'Chemistry'}
    """
    pass

def get_available_list_of_journals():
    """
    возвращает список всех журналов из базы в требуемом поддомене в
    формате [{'id': 'AASRI Procedia'}]
    """   


# get_total_list_of_domains('domains.json', 'physical-sciences-and-engineering')

# get_total_list_of_subdomains('domains.json', 'physical-sciences-and-engineering', 'energy')