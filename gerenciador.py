from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of war', 'Rack n Slash', 'PS2')
jogo3 = Jogo('The Witcher 3', 'RPG', 'PS5')
listaJogos = [jogo1, jogo2, jogo3]

app = Flask(__name__)
app.secret_key = 'itcio'

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
    if request.form['senha'] == "oi":
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' Usuário logado com sucesso')
        proximaPagina = request.form['proxima']
        if proximaPagina == "None":
            proximaPagina = ''

        return redirect('/{}'.format(proximaPagina))
        #return redirect(proximaPagina)
    else:
        flash('Usuário não logado com sucesso')
        return redirect(url_for('login'))


@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session['usuario_logado'] = None
    flash('logout efetuado com sucesso')
    return redirect(url_for('login'))

app.run(debug=True)