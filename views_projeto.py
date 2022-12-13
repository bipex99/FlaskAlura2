import os

from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from projetos import app, db
from models import Projetos
from helpers import recupera_imagem, deleta_arquivo, FormularioProjeto
import time

@app.route('/')
def index():
    lista = Projetos.query.order_by(Projetos.id)
    return render_template('lista.html', titulo='Projetos', projetos = lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioProjeto()
    return render_template('novo.html', titulo='Novo Projeto', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioProjeto(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    linguagem = form.linguagem.data
    descricao = form.descricao.data

    projeto = Projetos.query.filter_by(nome=nome).first()

    if projeto:
        flash('Projeto já existente')
        return redirect(url_for('index'))

    novo_projeto = Projetos(nome=nome, linguagem=linguagem, descricao=descricao)
    db.session.add(novo_projeto)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_projeto.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    projeto = Projetos.query.filter_by(id=id).first()
    form = FormularioProjeto()
    form.nome.data = projeto.nome
    form.linguagem.data = projeto.linguagem
    form.descricao.data = projeto.descricao
    capa_projeto = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Projeto', id=id, capa_projeto=capa_projeto, form=form)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioProjeto(request.form)

    if form.validate_on_submit():

        projeto = Projetos.query.filter_by(id=request.form['id']).first()
        projeto.nome = form.nome.data
        projeto.linguagem = form.linguagem.data
        projeto.descricao = form.descricao.data

        db.session.add(projeto)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(projeto.id)
        arquivo.save(f'{upload_path}/capa{projeto.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Projetos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Projeto deletado com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)