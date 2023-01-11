import os
from gerenciador import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField

class FormularioUsuario(FlaskForm):
    nome = StringField('Nome do Usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
    senha = StringField('Senha do Usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
    status = StringField('Status do Usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
    login = StringField('Login do Usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
    salvar = SubmitField('Salvar')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'foto{id}' in nome_arquivo:
            return nome_arquivo
    return 'semfoto.png'


def deleta_arquivos(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'semfoto.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'],arquivo))