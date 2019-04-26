from .collocation_handle import get_functions, db_adaptor
#import psycopg2
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/<primary_domain_url>')
def list_domains(primary_domain_url):
    primary_domains_list = [{'physical-sciences-and-engineering': 'Physical Sciences and Engineering'},
                            {'life-sciences': 'Life Sciences'},
                            {'health-sciences': 'Health Sciences'},
                            {'social-sciences-and-humanities': 'Social Sciences and Humanities'},
                            ]

    primary_domain_name = ''
    for primary_domain_dict in primary_domains_list:
        if primary_domain_url in primary_domain_dict.keys():
            primary_domain_name = primary_domain_dict[primary_domain_url]

    list_of_domains = db_adaptor.get_total_list_of_domains(
        'collocation_handle/domains.json', primary_domain_url)


    return render_template('domains-list.html',
                           primary_domain_name=primary_domain_name,
                           primary_domain_url=primary_domain_url,
                           list_of_subdomains=list_of_domains)


@app.route('/<super_domain_url>/<domain_url>/<subdomain_url>/<journal_id>')
def get_journal(super_domain_url, domain_url, subdomain_url, journal_id):
    super_domain_name = get_functions.url_form_to_name(super_domain_url)
    domain_name = get_functions.url_form_to_name(domain_url)
    subdomain_name = get_functions.url_form_to_name(subdomain_url)
    if not (super_domain_name & domain_name & subdomain_name):
        return render_template('404.html', text='Incorrect journal path')
    
    (output, journal_name) = get_functions.get_from_journal(journal_id)
    if output is None:
        return render_template('404.html', text='Incorrect journal id')

    names = {'super_domain': super_domain_name, 'domain': domain_name, 'subdomain': subdomain_name, 'journal': journal_name}

    return render_template('journal-graph.html', output=output, names=names)


@app.route('/domain/<name>')
def domain_view(name):
    return render_template('journal-graph.html')


@app.route('/<name>')
def primary_domain_view(name):
    """
    Вьюха для просмотра статистики по супердомену
    """
    
    (output, full_name) = get_functions.get_from_primary(name)
    if output is None:
        return 'Incorrect name'
    
    return render_template('primary_top_chart.html', output=output, name=full_name)