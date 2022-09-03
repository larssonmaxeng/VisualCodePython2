from app import app
from flask import render_template
@app.route('/')
@app.route('/index')
def index():
    nome = "dissertação1"
    criterio = {"nome":"Preço", "nota":"Médio"}
    return render_template('index.html', nome=nome, criterio=criterio)
@app.route('/contato')
def contato():
    return render_template('contato.html')        