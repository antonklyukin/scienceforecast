from . import connect
from .settings import DB_SETTINGS

import psycopg2
from multiprocessing import Pool


def find_repeating(result):
    unique_name_dict = {}
    repeating_id = {}
    for query in result:
        if query[1] not in unique_name_dict:
            unique_name_dict[query[1]] = query[0]
            repeating_id[query[0]] = []
        else:
            repeating_id[unique_name_dict[query[1]]].append(query[0])
    # print(repeating_id)
    return repeating_id



def delete_repeating_primary():
    (cur, connector) = connect.connect_to_db()
    cur.execute("SELECT id, name FROM primary_domains")
    result = cur.fetchall()
    repeating_id = find_repeating(result)
    for base_ident in repeating_id:        
        for repeating_ident in repeating_id[base_ident]:
            cur.execute("UPDATE domains SET primary_id = %s WHERE primary_id = %s", (base_ident, repeating_ident))
            cur.execute("DELETE FROM primary_domains WHERE id = %s", (repeating_ident,))
    connect.commit(cur, connector)

def delete_repeating_domains():
    (cur, connector) = connect.connect_to_db()
    cur.execute("SELECT id, name FROM domains")
    result = cur.fetchall()
    repeating_id = find_repeating(result)
    for base_ident in repeating_id:        
        for repeating_ident in repeating_id[base_ident]:
            cur.execute("UPDATE subdomains SET domain_id = %s WHERE domain_id = %s", (base_ident, repeating_ident))
            cur.execute("DELETE FROM domains WHERE id = %s", (repeating_ident,))
    connect.commit(cur, connector)

def delete_repeating_subdomains():
    (cur, connector) = connect.connect_to_db()
    cur.execute("SELECT id, name FROM subdomains")
    result = cur.fetchall()
    repeating_id = find_repeating(result)
    for base_ident in repeating_id:        
        for repeating_ident in repeating_id[base_ident]:
            cur.execute("UPDATE subdomains_journals SET subdomain_id = %s WHERE subdomain_id = %s", (base_ident, repeating_ident))
            cur.execute("DELETE FROM subdomains WHERE id = %s", (repeating_ident,))
    connect.commit(cur, connector)

def delete_repeating_collocations():
    (cur, connector) = connect.connect_to_db()
    cur.execute("SELECT id, collocation FROM collocations")
    result = cur.fetchall()
    cur.close()
    connector.close()
    repeating_id = find_repeating(result)
    pool_list = []
    for base_ident in repeating_id:
        if repeating_id[base_ident]:
            pool_list.append((base_ident, repeating_id[base_ident]))
    print(pool_list)
    pool_col = Pool(100)
    pool_col.map(collocation_repeating_delete, pool_list)
    


def collocation_repeating_delete(id_tuple):
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    print(id_tuple)
    for repeating_ident in id_tuple[1]:
        cur.execute("UPDATE articles_collocations SET collocation_id = %s WHERE collocation_id = %s", (id_tuple[0], repeating_ident))
        cur.execute("DELETE FROM collocations WHERE id = %s", (repeating_ident,))
    cur.close()
    connector.commit()
    connector.close()

def main():

    # delete_repeating_primary()
    # delete_repeating_domains()
    # delete_repeating_subdomains()
    delete_repeating_collocations()

    # delete_form_collocations()
    

if __name__ == '__main__':
    main()
    