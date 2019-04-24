from .collocation_handle import get_functions
#import psycopg2
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('journal-graph.html')


@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/domain/<name>')
def domain_view(name):
    return render_template('journal-graph.html')

@app.route('/primary/<name>')
def primary_domain_view(name):
    output = get_functions.get_from_primary(name)
    if output is None:
        return 'Incorrect name'
    return str(output)