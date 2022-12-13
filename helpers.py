import os
from projetos import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class FormularioProjeto(FlaskForm):
    nome = StringField('Nome do Projeto', [validators.DataRequired(), validators.Length(min=1, max=50)])
    linguagem = StringField('Linguagem', [validators.DataRequired(), validators.Length(min=1, max=40)])
    descricao = StringField('Descrição', [validators.DataRequired(), validators.Length(min=1, max=50)])
    salvar = SubmitField('Salvar')


class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'interrogacao.jpg'


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'interrogacao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))