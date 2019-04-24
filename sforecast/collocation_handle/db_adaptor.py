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
