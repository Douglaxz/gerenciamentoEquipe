# importação de dependencias
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
#from flask_sqlalchemy import SQLAlchemy
from gerenciador import app, db
from models import usuarios
from helpers import recupera_imagem

# rota index para mostrar os usuários
@app.route('/')
def index():
    lista = usuarios.query.order_by(usuarios.cod_usuario)
    return render_template('index.html', titulo='Usuários' , usuarios=lista)

# rota para criar novo formulário usuário 
@app.route('/novo')
def novo():
    if session['usuario_logado'] == None:
        #return redirect('/login?proxima=novo')
        return redirect(url_for('login',proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

# rota para criar novo formulário usuário 
@app.route('/editar/<int:id>')
def editar(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('editar')))
    usuario = usuarios.query.filter_by(cod_usuario=id).first()
    foto_usuario = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Usuário', usuario=usuario, foto_usuario=foto_usuario)    

# rota para criar novo usuário no banco de dados
@app.route('/criar', methods=['POST',])
def criar():
    nome  = request.form['nome']
    senha = request.form['senha']
    status = request.form['status']
    login = request.form['login']
    usuario = usuarios.query.filter_by(nome_usuario=nome).first()
    if usuario:
        flash ('Usuário já existe')
        return redirect(url_for('index')) 
    novoUsuario = usuarios(nome_usuario=nome, senha_usuario=senha, status_usuario=status, login_usuario=login )
    db.session.add(novoUsuario)
    db.session.commit()

    arquivo = request.files['arquivo']
    uploads_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{uploads_path}/foto{novoUsuario.cod_usuario}.jpg')

    return redirect(url_for('index'))

# rota para editar novo usuário no banco de dados
@app.route('/atualizar', methods=['POST',])
def atualizar():
    usuario = usuarios.query.filter_by(cod_usuario=request.form['id']).first()
    usuario.nome_usuario = request.form['nome']
    usuario.senha_usuario = request.form['senha']
    usuario.status_usuario = request.form['status']
    usuario.login_usuario = request.form['login']
    db.session.add(usuario)
    db.session.commit()

    arquivo = request.files['arquivo']
    uploads_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{uploads_path}/foto{usuario.cod_usuario}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login'))    
    usuarios.query.filter_by(cod_usuario=id).delete()
    db.session.commit()
    flash('Usuario apagado com sucesso!')
    return redirect(url_for('index'))    

# rota para a tela de login
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

# rota para autendicar a tela de login
@app.route('/autenticar', methods = ['GET', 'POST'])
def autenticar():
    usuario = usuarios.query.filter_by(login_usuario=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha_usuario:
            session['usuario_logado'] = usuario.login_usuario
            flash(usuario.nome_usuario + ' Usuário logado com sucesso')
            proximaPagina = request.form['proxima']
            if proximaPagina == "None":
                proximaPagina = ''
            return redirect('/{}'.format(proximaPagina))
        else:
            flash('Usuário não logado com sucesso')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado com sucesso')
        return redirect(url_for('login'))


# rota logout
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session['usuario_logado'] = None
    flash('logout efetuado com sucesso')
    return redirect(url_for('login'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads',nome_arquivo)