from flask import Flask, render_template, request, url_for, redirect, flash   
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.formulario

app = Flask(__name__)
app.secret_key="minha chave"
dados = []

@app.route('/')
def inicio():
    cadastro = db.cadastro
    return render_template('formulario/index.html', dados = cadastro.find())

@app.route('/cadastro')
def cadastro():
    return render_template('formulario/cadastro.html')

@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar():

    nome = request.form['nome']
    email = request.form['email']
    cidade = request.form['cidade']
    senha = request.form['senha']
    estado = request.form['estado']

    import uuid
    id = uuid.uuid3(uuid.NAMESPACE_DNS, email)
    id = str(id)[:5]
 
    if nome == '' or email == '' or cidade == '' or senha == '' or estado == '':
        flash('Preencha todos os campos.')
        return redirect(url_for('cadastro'))

    db.cadastro.insert_many([{'id': id, 'nome': nome, 'email': email, 'cidade': cidade, 'senha': senha, 'estado': estado}])    
    return redirect("/")

@app.route('/editar/<id>')
def editar(id):
    cadastro = db.cadastro
    dados = cadastro.find_one({'id': id})
    return render_template('formulario/editar.html', id = id, dados = dados)

@app.route('/editado/<id>', methods=['POST', 'GET'])
def editado(id):
    nome = request.form['nome']
    email = request.form['email']
    cidade = request.form['cidade']
    senha = request.form['senha']
    estado = request.form['estado']

    if nome == '' or email == '' or cidade == '' or senha == '' or estado == '':
        flash('Preencha todos os campos.')
        return redirect('/editar/'+id)

    alvo = { "id": id }
    novo = ([{"$set":  {'nome': nome, 'email': email, 'cidade': cidade, 'senha': senha, 'estado': estado}}])  

    db.cadastro.update_many(alvo, novo)
    return redirect("/")

@app.route('/apagar/<id>')
def apagar(id):
    db.cadastro.delete_one({'id': id})
    return redirect("/")

@app.route('/sobre')
def sobre():
    return render_template('formulario/sobre.html')