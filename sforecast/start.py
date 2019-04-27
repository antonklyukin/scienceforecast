from .collocation_handle import get_functions, db_adaptor
#import psycopg2
from flask import Flask, render_template
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

    list_of_domains = db_adaptor.get_total_list_of_domains(primary_domain_url)
    list_of_available_domains = db_adaptor.get_available_list_of_domains(primary_domain_name)
    for domain in list_of_domains:
        if domain[0] in list_of_available_domains:
            domain.append('Available')
        else:
            domain.append('Not Available')

    return render_template('domains-list.html',
                           primary_domain_name=primary_domain_name,
                           primary_domain_url=primary_domain_url,
                           list_of_domains=list_of_domains)


@app.route('/<super_domain_url>/<domain_url>')
def domain_view(super_domain_url, domain_url):
    return render_template('journal-graph.html')

@app.route('/<super_domain_url>/<domain_url>/<subdomain_url>')
def subdomain_view(super_domain_url, domain_url, subdomain_url):
    # Получение имен
    super_domain_name = get_functions.url_form_to_name(super_domain_url)
    domain_name = get_functions.url_form_to_name(domain_url)
    subdomain_name = get_functions.url_form_to_name(subdomain_url)
    return render_template('journal-graph.html')



@app.route('/<super_domain_url>/<domain_url>/<subdomain_url>/<journal_id>')
def get_journal(super_domain_url, domain_url, subdomain_url, journal_id):
    # Получение имен
    super_domain_name = get_functions.url_form_to_name(super_domain_url)
    domain_name = get_functions.url_form_to_name(domain_url)
    subdomain_name = get_functions.url_form_to_name(subdomain_url)
    if not (bool(super_domain_name) & bool(domain_name) & bool(subdomain_name)):
        return render_template('404.html', text='Incorrect journal path')
    
    result = get_functions.get_from_journal(journal_id)
    if result is None:
        return render_template('404.html', text='Incorrect journal id')
    output = result[0]
    journal_name = result[1]

    names = {'super_domain': super_domain_name, 'domain': domain_name, 'subdomain': subdomain_name, 'journal': journal_name}
    urls = {'super_domain': super_domain_url, 'domain': domain_url, 'subdomain': subdomain_url, 'journal': journal_id}

    return render_template('journal-graph.html', output=output, names=names, urls=urls)

