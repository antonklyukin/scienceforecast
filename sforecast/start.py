from .collocation_handle import get_functions
#import psycopg2
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/subdomains')
def subdomains():
    return render_template('domains-list.html')


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