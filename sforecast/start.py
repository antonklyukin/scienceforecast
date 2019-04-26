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

@app.route('/journal')
def journal():
    return render_template('journal-graph.html')


@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/domain/<name>')
def domain_view(name):
    return render_template('journal-graph.html')

@app.route('/primary/<name>')
def primary_domain_view(name):
    """
    Вьюха для просмотра статистики по супердомену
    """
    output = get_functions.get_from_primary(name)
    if output is None:
        return 'Incorrect name'
    return render_template('primary_top_chart.html', output=output)