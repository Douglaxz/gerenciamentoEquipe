from flask import Flask, render_template, request, redirect, session, flash, url_for
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Douglas Amaral", "douglas", "1")
usuario2 = Usuario("Francieli Amaral", "francieli", "1")
usuario3 = Usuario("Lila", "lila", "1")
usuario4 = Usuario("Melvim", "melvim", "1")
usuarios = { usuario1.nickname: usuario1,
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3,
            usuario4.nickname: usuario4
            }

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of war', 'Rack n Slash', 'PS2')
jogo3 = Jogo('The Witcher 3', 'RPG', 'PS5')
listaJogos = [jogo1, jogo2, jogo3]

app = Flask(__name__)
app.secret_key = 'itcio'

#engine = create_engine("mysql:///?User=myUser&Password=myPassword&Database=NorthWind&Server=myServer&Port=3306")
#engine = create_engine("mysql+pymysql://usrnme:passwd@hstnme/dbname")
engine = create_engine("mysql+pymysql://root:admin@localhost/gerenciador")

#app.config['SQLALCHEMY_DATABASE_URI'] = \
#    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
#        SGBD_=_'mysql+mysqlconnector',
#        usuario_=_'root',
#        senha_=_'admin',
#        servidor_=_'127.0.0.1',
#        database_=_'gerenciador')
#
#db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html', titulo='jogos' , jogos=listaJogos)

@app.route('/novo')
def novo():
    if session['usuario_logado'] == None:
        return redirect('/login?proxima=novo')
        return redirect(url_for('login',proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome  =request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    listaJogos.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods = ['GET', 'POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' Usuário logado com sucesso')
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



@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session['usuario_logado'] = None
    flash('logout efetuado com sucesso')
    return redirect(url_for('login'))

app.run(debug=True)