#importações
import os
from gerenciador import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField,IntegerField, SelectField

##------------------------------------------------------------------------------------------------------------------------------
# USUÁRIO
##------------------------------------------------------------------------------------------------------------------------------

#criação via wftorm do formulario de usuarios
class FormularioUsuario(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=50)])
    senha = IntegerField('Senha', [validators.DataRequired(), validators.Length(min=1, max=50)])
    status = StringField('Status', [validators.DataRequired(), validators.Length(min=1, max=50)])
    login = StringField('Login', [validators.DataRequired(), validators.Length(min=1, max=50)])
    salvar = SubmitField('Salvar')

#criação via wftorm do formulario de usuarios
class FormularioUsuarioVisualizar(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={'readonly': True})
    senha = IntegerField('Senha', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = StringField('Status', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    login = StringField('Login', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    salvar = SubmitField('Editar')    

#------------------------------------------------------------------------------------------------------------------------------
# USUÁRIO
#------------------------------------------------------------------------------------------------------------------------------

#criação via wftorm do formulario de tipo usuarios
class FormularioTipoUsuarioEdicao(FlaskForm):
    descricao = StringField('Descrição', [validators.DataRequired(), validators.Length(min=1, max=50)])
    status = SelectField('Situação', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#criação via wftorm do formulario de tipo usuarios
class FormularioTipoUsuarioVisualizar(FlaskForm):
    descricao = StringField('Descrição', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')    

#------------------------------------------------------------------------------------------------------------------------------
# OUTROS
#------------------------------------------------------------------------------------------------------------------------------
#classe de upload de imagem (desativada no momento)
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'foto{id}' in nome_arquivo:
            return nome_arquivo
    return 'semfoto.png'

#classe de apagar fotos duplicadas de usuarios (desativada no momento)
def deleta_arquivos(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'semfoto.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'],arquivo))