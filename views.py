# importação de dependencias
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from gerenciador import app, db
from models import tb_usuarios, \
    tb_tipousuario, \
    tb_beneficios, \
    tb_areas, \
    tb_tipolancamento, \
    tb_beneficiousuario,\
    tb_periodos,\
    tb_periodofuncionario
from helpers import recupera_imagem,deleta_arquivos, \
    FormularioPeriodoEdicao, \
    FormularioPeriodoVisualizar, \
    FormularioBeneficioUsuarioVisualizacao, \
    FormularioBeneficioUsuarioEdicao, \
    FormularPesquisa, \
    FormularioUsuario, \
    FormularioUsuarioVisualizar, \
    FormularioTipoUsuarioEdicao,\
    FormularioTipoUsuarioVisualizar, \
    FormularioBeneficiosEdicao, \
    FormularioBeneficiosVisualizar, \
    FormularioAreaEdicao,\
    FormularioAreaVisualizar,\
    FormularioTipoLancamentoVisualizar,\
    FormularioTipoLancamentoEdicao,\
    FormularioLancamentoVisualizar,\
    FormularioLancamentoEdicao,\
    FormularioPesquisaPeriodo
import time
from datetime import date, timedelta

# rota index
@app.route('/')
def index():
    #if session['usuario_logado'] == None:
    #    return redirect(url_for('login',proxima=url_for('novoUsuario')))    
    return render_template('index.html', titulo='Bem vindos')

# rota logout
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session['usuario_logado'] = None
    flash('logout efetuado com sucesso')
    return redirect(url_for('login'))

# rota para a tela de login
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

# rota para autendicar a tela de login
@app.route('/autenticar', methods = ['GET', 'POST'])
def autenticar():
    usuario = tb_usuarios.query.filter_by(login_usuario=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha_usuario:
            session['usuario_logado'] = usuario.login_usuario
            session['nomeusuario_logado'] = usuario.nome_usuario
            session['tipousuario_logado'] = usuario.cod_tipousuario
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


#---------------------------------------------------------------------------------------------------------------------------------
#USUARIOS
#---------------------------------------------------------------------------------------------------------------------------------

# rota index para mostrar os usuários
@app.route('/usuario')
def usuario():
    form = FormularPesquisa()
    page = request.args.get('page', 1, type=int)
    usuarios = tb_usuarios.query\
    .join(tb_areas, tb_areas.cod_area==tb_usuarios.cod_area)\
    .join(tb_tipousuario, tb_tipousuario.cod_tipousuario==tb_usuarios.cod_tipousuario)\
    .add_columns(tb_usuarios.login_usuario, tb_usuarios.cod_usuario, tb_usuarios.nome_usuario, tb_usuarios.status_usuario, tb_areas.desc_area, tb_tipousuario.desc_tipousuario)\
    .order_by(tb_usuarios.nome_usuario)\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios, form=form)

# rota index para mostrar pesquisa usuários
@app.route('/usuarioPesquisa', methods=['POST',])
def usuarioPesquisa():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()
    usuarios = tb_usuarios.query\
    .filter(tb_usuarios.nome_usuario.ilike(f'%{form.pesquisa.data}%'))\
    .join(tb_areas, tb_areas.cod_area==tb_usuarios.cod_area)\
    .join(tb_tipousuario, tb_tipousuario.cod_tipousuario==tb_usuarios.cod_tipousuario)\
    .add_columns(tb_usuarios.login_usuario, tb_usuarios.cod_usuario, tb_usuarios.nome_usuario, tb_usuarios.status_usuario, tb_areas.desc_area, tb_tipousuario.desc_tipousuario)\
    .order_by(tb_usuarios.nome_usuario)\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('usuarios.html', titulo='Usuários' , usuarios=usuarios, form=form)

# rota para criar novo formulário usuário 
@app.route('/novoUsuario')
def novoUsuario():
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('novoUsuario')))
    form = FormularioUsuario()
    return render_template('novoUsuario.html', titulo='Novo Usuário', form=form)

# rota para visualizar usuário 
@app.route('/visualizarUsuario/<int:id>')
def visualizarUsuario(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarUsuario')))
    usuario = tb_usuarios.query.filter_by(cod_usuario=id).first()
    form = FormularioUsuarioVisualizar()
    form.nome.data = usuario.nome_usuario
    form.senha.data = usuario.senha_usuario
    form.status.data = usuario.status_usuario
    form.login.data = usuario.login_usuario
    form.tipousuario.data = usuario.cod_tipousuario
    form.area.data = usuario.cod_area
    form1 = FormularioBeneficioUsuarioVisualizacao()
    beneficiosusuario = tb_beneficiousuario.query.filter_by(cod_usuario=id)\
        .join(tb_beneficios, tb_beneficios.cod_beneficio==tb_beneficiousuario.cod_beneficio)\
        .add_columns(tb_beneficios.desc_beneficio,tb_beneficiousuario.cod_beneficiousuario)
    return render_template('visualizarUsuario.html', titulo='Visualizar Usuário', id=id, form=form, form1=form1, beneficiosusuario=beneficiosusuario)   

# rota para editar formulário usuário 
@app.route('/editarUsuario/<int:id>')
def editarUsuario(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarUsuario')))
    usuario = tb_usuarios.query.filter_by(cod_usuario=id).first()
    form = FormularioUsuario()
    form.nome.data = usuario.nome_usuario
    form.senha.data = usuario.senha_usuario
    form.status.data = usuario.status_usuario
    form.login.data = usuario.login_usuario
    form.tipousuario.data = usuario.cod_tipousuario
    form.area.data = usuario.cod_area
    return render_template('editarUsuario.html', titulo='Editar Usuário', id=id, form=form)    
       
# rota para criar usuário no banco de dados
@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioUsuario(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novo'))
    nome  = form.nome.data
    senha = form.senha.data
    status = form.status.data
    login = form.login.data
    tipousuario = form.tipousuario.data
    area = form.area.data
    usuario = tb_usuarios.query.filter_by(nome_usuario=nome).first()
    if usuario:
        flash ('Usuário já existe')
        return redirect(url_for('index')) 
    novoUsuario = tb_usuarios(nome_usuario=nome, senha_usuario=senha, status_usuario=status, login_usuario=login, cod_tipousuario=tipousuario, cod_area=area)
    db.session.add(novoUsuario)
    db.session.commit()

    #arquivo = request.files['arquivo']
    #uploads_path = app.config['UPLOAD_PATH']
    #timestamp = time.time
    #deleta_arquivos(usuario.cod_usuario)
    #arquivo.save(f'{uploads_path}/foto{usuario.cod_usuario}-{timestamp}.jpg')

    return redirect(url_for('usuario'))

# rota para atualizar usuário no banco de dados
@app.route('/atualizarUsuario', methods=['POST',])
def atualizarUsuario():
    form = FormularioUsuario(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        usuario = tb_usuarios.query.filter_by(cod_usuario=request.form['id']).first()
        usuario.nome_usuario = form.nome.data
        usuario.senha_usuario = form.senha.data
        usuario.status_usuario = form.status.data
        usuario.login_usuario = form.login.data
        usuario.cod_tipousuario = form.tipousuario.data
        usuario.cod_area = form.area.data
        db.session.add(usuario)
        db.session.commit()
    return redirect(url_for('visualizarUsuario', id=id))

# rota para deletar usuário no banco de dados
@app.route('/deletarUsuario/<int:id>')
def deletarUsuario(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login'))    
    tb_usuarios.query.filter_by(cod_usuario=id).delete()
    db.session.commit()
    flash('Usuario apagado com sucesso!')
    return redirect(url_for('usuario'))    

# rota para upload de fotos de usuário no banco de dados (desativado)
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads',nome_arquivo)

#---------------------------------------------------------------------------------------------------------------------------------
#TIPO USUARIOS
#---------------------------------------------------------------------------------------------------------------------------------

# rota index para mostrar os tipo usuários
@app.route('/tipousuario')
def tipousuario():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()    
    tiposusuario = tb_tipousuario.query.order_by(tb_tipousuario.cod_tipousuario)\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('tipousuarios.html', titulo='Tipo Usuários', tiposusuario=tiposusuario, form=form)

# rota index para mostrar pesquisa dos tipo usuários
@app.route('/tipousuarioPesquisa', methods=['POST',])
def tipousuarioPesquisa():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()
    tiposusuario = tb_tipousuario.query.order_by(tb_tipousuario.desc_tipousuario)\
    .filter(tb_tipousuario.desc_tipousuario.ilike(f'%{form.pesquisa.data}%'))\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('tipousuarios.html', titulo='Tipo Usuários' , tiposusuario=tiposusuario, form=form)    

# rota para criar novo formulário usuário 
@app.route('/novoTipoUsuario')
def novoTipoUsuario():
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('novoTipoUsuario')))
    form = FormularioTipoUsuarioEdicao()
    return render_template('novoTipoUsuario.html', titulo='Novo Tipo Usuário', form=form)

# rota para criar tipo usuário no banco de dados
@app.route('/criarTipoUsuario', methods=['POST',])
def criarTipoUsuario():
    form = FormularioTipoUsuarioEdicao(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('criarTipoUsuario'))
    desc  = form.descricao.data
    status = form.status.data
    tipousuario = tb_tipousuario.query.filter_by(desc_tipousuario=desc).first()
    if tipousuario:
        flash ('Tipo Usuário já existe')
        return redirect(url_for('tipousuario')) 
    novoTipoUsuario = tb_tipousuario(desc_tipousuario=desc, status_tipousuario=status)
    db.session.add(novoTipoUsuario)
    db.session.commit()
    return redirect(url_for('tipousuario'))

# rota para visualizar tipo usuário 
@app.route('/visualizarTipoUsuario/<int:id>')
def visualizarTipoUsuario(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarTipoUsuario')))
    tipousuario = tb_tipousuario.query.filter_by(cod_tipousuario=id).first()
    form = FormularioTipoUsuarioVisualizar()
    form.descricao.data = tipousuario.desc_tipousuario
    form.status.data = tipousuario.status_tipousuario
    return render_template('visualizarTipoUsuario.html', titulo='Visualizar Tipo Usuário', id=id, form=form)   

# rota para editar formulário tipo usuário 
@app.route('/editarTipoUsuario/<int:id>')
def editarTipoUsuario(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarTipoUsuario')))
    tipousuario = tb_tipousuario.query.filter_by(cod_tipousuario=id).first()
    form = FormularioTipoUsuarioEdicao()
    form.descricao.data = tipousuario.desc_tipousuario
    form.status.data = tipousuario.status_tipousuario
    return render_template('editarTipoUsuario.html', titulo='Editar Tipo Usuário', id=id, form=form)   

# rota para atualizar usuário no banco de dados
@app.route('/atualizarTipoUsuario', methods=['POST',])
def atualizarTipoUsuario():
    form = FormularioTipoUsuarioEdicao(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        tipousuario = tb_tipousuario.query.filter_by(cod_tipousuario=request.form['id']).first()
        tipousuario.desc_tipousuario = form.descricao.data
        tipousuario.status_tipousuario = form.status.data
        db.session.add(tipousuario)
        db.session.commit()
    return redirect(url_for('visualizarTipoUsuario', id=id))    

# rota para deletar usuário no banco de dados
@app.route('/deletarTipoUsuario/<int:id>')
def deletarTipoUsuario(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login'))    
    tb_tipousuario.query.filter_by(cod_tipousuario=id).delete()
    db.session.commit()
    flash('Tipo Usuario apagado com sucesso!')
    return redirect(url_for('tipousuario'))    

#---------------------------------------------------------------------------------------------------------------------------------
#BENEFICIOS
#---------------------------------------------------------------------------------------------------------------------------------
# rota index para mostrar os beneficios
@app.route('/beneficio')
def beneficio():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()    
    beneficios = tb_beneficios.query.order_by(tb_beneficios.desc_beneficio)\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('beneficios.html', titulo='Beneficios', beneficios=beneficios, form=form)

# rota index para pesquisar os beneficios
@app.route('/beneficioPesquisa', methods=['POST',])
def beneficioPesquisa():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()
    lista = tb_beneficios.query.order_by(tb_beneficios.desc_beneficio)\
    .filter(tb_beneficios.desc_beneficio.ilike(f'%{form.pesquisa.data}%'))\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('beneficios.html', titulo='Benefícios' , lista=lista, form=form)

# rota para criar novo formulário usuário 
@app.route('/novoBeneficio')
def novoBeneficio():
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('novoBeneficio')))
    form = FormularioBeneficiosEdicao()
    return render_template('novoBeneficio.html', titulo='Novo Beneficio', form=form)

# rota para criar beneficio no banco de dados
@app.route('/criarBeneficio', methods=['POST',])
def criarBeneficio():
    form = FormularioBeneficiosEdicao(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novoBeneficio'))
    desc  = form.descricao.data
    status = form.status.data
    beneficio = tb_beneficios.query.filter_by(desc_beneficio=desc).first()
    if beneficio:
        flash ('Beneficio já existe')
        return redirect(url_for('beneficios')) 
    novoBeneficio= tb_beneficios(desc_beneficio=desc, status_beneficio=status)
    db.session.add(novoBeneficio)
    db.session.commit()
    return redirect(url_for('beneficio'))   

# rota para visualizar beneficios 
@app.route('/visualizarBeneficio/<int:id>')
def visualizarBeneficio(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarBeneficios')))
    beneficio = tb_beneficios.query.filter_by(cod_beneficio=id).first()
    form = FormularioBeneficiosVisualizar()
    form.descricao.data = beneficio.desc_beneficio
    form.status.data = beneficio.status_beneficio
    return render_template('visualizarBeneficio.html', titulo='Visualizar Beneficio', id=id, form=form)  

# rota para editar formulário beneficio
@app.route('/editarBeneficio/<int:id>')
def editarBeneficio(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarBeneficio')))
    beneficio = tb_beneficios.query.filter_by(cod_beneficio=id).first()
    form = FormularioBeneficiosEdicao()
    form.descricao.data = beneficio.desc_beneficio
    form.status.data = beneficio.status_beneficio
    return render_template('editarBeneficio.html', titulo='Editar Beneficio', id=id, form=form)   

# rota para atualizar beneficio no banco de dados
@app.route('/atualizarBeneficio', methods=['POST',])
def atualizarBeneficio():
    form = FormularioBeneficiosEdicao(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        beneficio = tb_beneficios.query.filter_by(cod_beneficio=request.form['id']).first()
        beneficio.desc_beneficio = form.descricao.data
        beneficio.status_beneficio = form.status.data
        db.session.add(beneficio)
        db.session.commit()
    return redirect(url_for('visualizarBeneficio', id=id))    

# rota para deletar beneficio no banco de dados
@app.route('/deletarBeneficio/<int:id>')
def deletarBeneficio(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login'))    
    tb_beneficios.query.filter_by(cod_beneficio=id).delete()
    db.session.commit()
    flash('Beneficio apagado com sucesso!')
    return redirect(url_for('beneficio'))  

#---------------------------------------------------------------------------------------------------------------------------------
#AREAS
#---------------------------------------------------------------------------------------------------------------------------------
# rota index para mostrar os area
@app.route('/area')
def area():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()
    areas = tb_areas.query.order_by(tb_areas.cod_area)\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('areas.html', titulo='Áreas', areas=areas, form=form)

# rota index para pesquisar áreas
@app.route('/areaPesquisa', methods=['POST',])
def areaPesquisa():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()
    areas = tb_areas.query.order_by(tb_areas.desc_area)\
    .filter(tb_areas.desc_area.ilike(f'%{form.pesquisa.data}%'))\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('areas.html', titulo='Áreas' , areas=areas, form=form)

# rota para criar novo formulário area 
@app.route('/novoArea')
def novoArea():
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('novoArea')))
    form = FormularioAreaEdicao()
    return render_template('novoArea.html', titulo='Novo Area', form=form)

# rota para criar area no banco de dados
@app.route('/criarArea', methods=['POST',])
def criarArea():
    form = FormularioAreaEdicao(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novoArea'))
    desc  = form.descricao.data
    status = form.status.data
    area = tb_areas.query.filter_by(desc_area=desc).first()
    if area:
        flash ('Área já existe')
        return redirect(url_for('areas')) 
    novoArea= tb_areas(desc_area=desc, status_area=status)
    db.session.add(novoArea)
    db.session.commit()
    return redirect(url_for('area'))   

# rota para visualizar area 
@app.route('/visualizarArea/<int:id>')
def visualizarArea(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarArea')))
    area = tb_areas.query.filter_by(cod_area=id).first()
    form = FormularioAreaVisualizar()
    form.descricao.data = area.desc_area
    form.status.data = area.status_area
    return render_template('visualizarArea.html', titulo='Visualizar Área', id=id, form=form)  

# rota para editar formulário area
@app.route('/editarArea/<int:id>')
def editarArea(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarArea')))
    area = tb_areas.query.filter_by(cod_area=id).first()
    form = FormularioAreaEdicao()
    form.descricao.data = area.desc_area
    form.status.data = area.status_area
    return render_template('editarArea.html', titulo='Editar Area', id=id, form=form)   

# rota para atualizar area no banco de dados
@app.route('/atualizarArea', methods=['POST',])
def atualizarArea():
    form = FormularioAreaEdicao(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        area = tb_areas.query.filter_by(cod_area=request.form['id']).first()
        area.desc_area = form.descricao.data
        area.status_area = form.status.data
        db.session.add(area)
        db.session.commit()
    return redirect(url_for('visualizarArea', id=id))    

# rota para deletar area no banco de dados
@app.route('/deletarArea/<int:id>')
def deletarArea(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login'))    
    tb_areas.query.filter_by(cod_area=id).delete()
    db.session.commit()
    flash('Área apagado com sucesso!')
    return redirect(url_for('area')) 

#---------------------------------------------------------------------------------------------------------------------------------
#TIPO LANÇAMENTO
#---------------------------------------------------------------------------------------------------------------------------------
# rota index para mostrar os tipo lancamento
@app.route('/tipolancamento')
def tipolancamento():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()    
    tiposlancamento = tb_tipolancamento.query.order_by(tb_tipolancamento.desc_tipolancamento)\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('tiposlancamento.html', titulo='Tipo Lançamento', tiposlancamento=tiposlancamento, form=form)

# rota index para pesquisar tipos de lançamento
@app.route('/tipolancamentoPesquisa', methods=['POST',])
def tipolancamentoPesquisa():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()
    tiposlancamento = tb_tipolancamento.query.order_by(tb_tipolancamento.desc_tipolancamento)\
    .filter(tb_tipolancamento.desc_tipolancamento.ilike(f'%{form.pesquisa.data}%'))\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('tiposlancamento.html', titulo='Tipo Lançamento' , tiposlancamento=tiposlancamento, form=form)

# rota para criar novo formulário tipo lancamento
@app.route('/novoTipoLancamento')
def novoTipoLancamento():
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('novoTipoLancamento')))
    form = FormularioTipoLancamentoEdicao()
    return render_template('novoTipoLancamento.html', titulo='Novo Tipo Lançamento', form=form)

# rota para criar tipo lancamento no banco de dados
@app.route('/criarTipoLancamento', methods=['POST',])
def criarTipoLancamento():
    form = FormularioTipoLancamentoEdicao(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novoTipoLancamento'))
    sigla  = form.sigla.data
    desc  = form.descricao.data
    status = form.status.data
    tipolancamento = tb_tipolancamento.query.filter_by(desc_tipolancamento=desc).first()
    if tipolancamento:
        flash ('TipoLancamento já existe')
        return redirect(url_for('tipolancamento')) 
    novoTipoLancamento= tb_tipolancamento(desc_tipolancamento=desc, status_tipolancamento=status, sigla_tipolancamento=sigla)
    db.session.add(novoTipoLancamento)
    db.session.commit()
    return redirect(url_for('tipolancamento'))   

# rota para visualizar tipo lancamento 
@app.route('/visualizarTipoLancamento/<int:id>')
def visualizarTipoLancamento(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarTipoLancamento')))
    tipolancamento = tb_tipolancamento.query.filter_by(cod_tipolancamento=id).first()
    form = FormularioTipoLancamentoVisualizar()
    form.sigla.data = tipolancamento.sigla_tipolancamento
    form.descricao.data = tipolancamento.desc_tipolancamento
    form.status.data = tipolancamento.status_tipolancamento
    return render_template('visualizarTipoLancamento.html', titulo='Visualizar Tipo Lançamento', id=id, form=form)  

# rota para editar formulário tipo lançamento
@app.route('/editarTipoLancamento/<int:id>')
def editarTipoLancamento(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarTipoLancamento')))
    tipolancamento = tb_tipolancamento.query.filter_by(cod_tipolancamento=id).first()
    form = FormularioTipoLancamentoEdicao()
    form.sigla.data = tipolancamento.sigla_tipolancamento
    form.descricao.data = tipolancamento.desc_tipolancamento
    form.status.data = tipolancamento.status_tipolancamento
    return render_template('editarTipoLancamento.html', titulo='Editar Tipo Lançamento', id=id, form=form)   

# rota para atualizar tipo lancamento no banco de dados
@app.route('/atualizarTipoLancamento', methods=['POST',])
def atualizarTipoLancamento():
    form = FormularioTipoLancamentoEdicao(request.form)

    if form.validate_on_submit():
        id = request.form['id']
        tipolancamento = tb_tipolancamento.query.filter_by(cod_tipolancamento=request.form['id']).first()
        tipolancamento.sigla_tipolancamento = form.sigla.data
        tipolancamento.desc_tipolancamento = form.descricao.data
        tipolancamento.status_tipolancamento = form.status.data

        db.session.add(tipolancamento)
        db.session.commit()

    return redirect(url_for('visualizarTipoLancamento', id=id))    

# rota para deletar tipo lancamento no banco de dados
@app.route('/deletarTipoLancamento/<int:id>')
def deletarTipoLancamento(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('tipolancamento'))    
    tb_tipolancamento.query.filter_by(cod_tipolancamento=id).delete()
    db.session.commit()
    flash('Tipo Lançamento apagado com sucesso!')
    return redirect(url_for('tipolancamento')) 

#---------------------------------------------------------------------------------------------------------------------------------
#BENEFICIO USUARIOS
#---------------------------------------------------------------------------------------------------------------------------------
# rota para criar novo formulário beneficio funcionario 
@app.route('/novoBeneficioUsuario/<int:id>')
def novoBeneficioUsuario(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('novoTipoUsuario')))
    form = FormularioBeneficioUsuarioEdicao()
    return render_template('novoBeneficioUsuario.html', titulo='Novo Beneficio Usuário', form=form, id=id)

# rota para criar beneficio do funcionario no banco de dados
@app.route('/criarBeneficioUsuario/<int:id>', methods=['POST',])
def criarBeneficioUsuario(id):
    form = FormularioBeneficioUsuarioEdicao(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novoBeneficioUsuario',id=id))
    beneficio  = form.beneficio.data
    usuario = id
    beneficiousuario = tb_beneficiousuario.query.filter_by(cod_usuario=id, cod_beneficio=beneficio).first()
    if beneficiousuario:
        flash ('Beneficio já cadastrado para esse usuário')
        return redirect(url_for('visualizarUsuario',id=id)) 
    novoBeneficioUsuario = tb_beneficiousuario(cod_usuario=usuario, cod_beneficio=beneficio)
    db.session.add(novoBeneficioUsuario)
    db.session.commit()
    return redirect(url_for('visualizarUsuario',id=id)) 

# rota para deletar beneficio do funcionario no banco de dados
@app.route('/deletarBeneficioUsuario/<int:id><int:beneficiousuario>')
def deletarBeneficioUsuario(id,beneficiousuario):
    if session['usuario_logado'] == None:
        return redirect(url_for('login'))    
    tb_beneficiousuario.query.filter_by(cod_beneficiousuario=beneficiousuario).delete()
    db.session.commit()
    flash('Beneficio apagado com sucesso!')
    return redirect(url_for('visualizarUsuario',id=id)) 

#---------------------------------------------------------------------------------------------------------------------------------
#PERÍODO
#---------------------------------------------------------------------------------------------------------------------------------
# rota index para mostrar os periodo
@app.route('/periodo')
def periodo():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()    
    periodos = tb_periodos.query.order_by(tb_periodos.desc_periodo)\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('periodos.html', titulo='Períodos', periodos=periodos, form=form)

# rota index para pesquisar os periodo pesquisa
@app.route('/periodoPesquisa', methods=['POST',])
def periodoPesquisa():
    page = request.args.get('page', 1, type=int)
    form = FormularPesquisa()
    periodos = tb_periodos.query.order_by(tb_periodos.desc_periodo)\
    .filter(tb_periodos.desc_periodo.ilike(f'%{form.pesquisa.data}%'))\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('periodos.html', titulo='Período' , periodos=periodos, form=form)

# rota para criar novo formulário periodo
@app.route('/novoPeriodo')
def novoPeriodo():
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('novoPeriodo')))
    form = FormularioPeriodoEdicao()
    return render_template('novoPeriodo.html', titulo='Novo Período', form=form)

# rota para criar periodo no banco de dados
@app.route('/criarPeriodo', methods=['POST',])
def criarPeriodo():
    form = FormularioPeriodoEdicao(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novoPeriodo'))
    desc  = form.descricao.data
    status = form.status.data
    inicio  = form.inicio.data
    final = form.final.data
    periodo = tb_periodos.query.filter_by(desc_periodo=desc).first()
    if periodo:
        flash ('Periodo já existe')
        return redirect(url_for('periodo')) 
    novoPeriodo= tb_periodos(desc_periodo=desc, status_periodo=status, inicio_periodo=inicio, final_periodo=final)
    db.session.add(novoPeriodo)
    db.session.commit()
    return redirect(url_for('periodo'))   

# rota para visualizar periodo
@app.route('/visualizarPeriodo/<int:id>')
def visualizarPeriodo(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarPeriodo')))
    periodo = tb_periodos.query.filter_by(cod_periodo=id).first()
    form = FormularioPeriodoVisualizar()
    form.descricao.data = periodo.desc_periodo
    form.status.data = periodo.status_periodo
    form.inicio.data = periodo.inicio_periodo
    form.final.data = periodo.final_periodo
    return render_template('visualizarPeriodo.html', titulo='Visualizar Periodo', id=id, form=form)  

# rota para editar formulário periodo
@app.route('/editarPeriodo/<int:id>')
def editarPeriodo(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarPeriodo')))
    periodo = tb_periodos.query.filter_by(cod_periodo=id).first()
    form = FormularioPeriodoEdicao()
    form.descricao.data = periodo.desc_periodo
    form.status.data = periodo.status_periodo
    form.inicio.data = periodo.inicio_periodo
    form.final.data = periodo.final_periodo
    return render_template('editarPeriodo.html', titulo='Editar Periodo', id=id, form=form)   

# rota para atualizar periodo no banco de dados
@app.route('/atualizarPeriodo/<int:id>', methods=['POST',])
def atualizarPeriodo(id):
    form = FormularioPeriodoEdicao(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        periodo = tb_periodos.query.filter_by(cod_periodo=request.form['id']).first()
        periodo.desc_periodo = form.descricao.data
        periodo.status_periodo = form.status.data
        periodo.inicio_periodo = form.inicio.data
        periodo.final_periodo = form.final.data
        db.session.add(periodo)
        db.session.commit()
    return redirect(url_for('visualizarPeriodo', id=id))  

# rota para deletar periodo no banco de dados
@app.route('/deletarPeriodo/<int:id>')
def deletarPeriodo(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login'))    
    tb_periodos.query.filter_by(cod_periodo=id).delete()
    db.session.commit()
    flash('Periodo apagado com sucesso!')
    return redirect(url_for('periodo',id=id)) 

#---------------------------------------------------------------------------------------------------------------------------------
#FUNCIONARIOS
#---------------------------------------------------------------------------------------------------------------------------------    
# rota index para mostrar os usuários
@app.route('/funcionario')
def funcionario():
    form = FormularPesquisa()
    page = request.args.get('page', 1, type=int)
    funcionarios = tb_usuarios\
    .query.filter_by(status_usuario=0)\
    .join(tb_areas, tb_areas.cod_area==tb_usuarios.cod_area)\
    .join(tb_tipousuario, tb_tipousuario.cod_tipousuario==tb_usuarios.cod_tipousuario)\
    .add_columns(tb_usuarios.login_usuario, tb_usuarios.cod_usuario, tb_usuarios.nome_usuario, tb_usuarios.status_usuario, tb_areas.desc_area, tb_tipousuario.desc_tipousuario)\
    .order_by(tb_usuarios.nome_usuario)\
    .paginate(page=page, per_page=5, error_out=False)
    return render_template('funcionarios.html', titulo='Profissionais', funcionarios=funcionarios, form=form)

# rota para visualizar funcionario 
@app.route('/visualizarFuncionario/<int:id>')
def visualizarFuncionario(id):
    if session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('visualizarFuncionario')))
    funcionario = tb_usuarios.query.filter_by(cod_usuario=id).first()
    form = FormularioUsuarioVisualizar()
    form.nome.data = funcionario.nome_usuario
    form.area.data = funcionario.cod_area
    periodos = tb_periodos.query.filter_by(status_periodo=0)
    return render_template('visualizarFuncionario.html', titulo='Visualizar Profissional', id=id, form=form, periodos=periodos)   

# rota para incluir periodo para o usuario no banco de dados
@app.route('/novoPeriodoFuncionario/<int:id><int:periodo>')
def novoPeriodoFuncionario(id,periodo):
    if session['usuario_logado'] == None:
        return redirect(url_for('login'))    
    periodolancamento = tb_periodos.query.filter_by(cod_periodo=periodo).first()
    if periodolancamento:
        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)#
        start_date = (periodolancamento.inicio_periodo)
        end_date = (periodolancamento.final_periodo)+ timedelta(days=1)  
        periodolancamentoFuncionario = tb_periodofuncionario.query.filter_by(cod_periodo=periodo, cod_usuario=id).first()
        if not periodolancamentoFuncionario:
            for single_date in daterange(start_date, end_date):
                if (single_date.weekday() < 5):
                    novoPeriodoFuncionario= tb_periodofuncionario(cod_usuario=id, cod_periodo=periodo, cod_tipolancamento=7, data_periodoFuncionario=single_date)
                    db.session.add(novoPeriodoFuncionario)
                    db.session.commit()
            return redirect(url_for('visualizarFuncionario',id=id))
        else:
            return redirect(url_for('visualizarLancamentoFuncionario',id=id,periodo=periodo))

# rota para visualizar lancamento do funcionario no banco de dados
@app.route('/visualizarLancamentoFuncionario/<int:id><int:periodo>')
def visualizarLancamentoFuncionario(id,periodo):
    form = FormularioLancamentoEdicao()    
    lancamentos = tb_periodofuncionario\
                .query.filter_by(cod_periodo=periodo, cod_usuario=id)\
                .join(tb_tipolancamento, tb_tipolancamento.cod_tipolancamento==tb_periodofuncionario.cod_tipolancamento)\
                .add_columns(tb_periodofuncionario.data_periodoFuncionario, tb_periodofuncionario.cod_periodoFuncionario, tb_tipolancamento.sigla_tipolancamento, tb_tipolancamento.desc_tipolancamento)\
                .order_by(tb_periodofuncionario.data_periodoFuncionario)
    return render_template('editarLancamentoPeriodos.html', titulo='Lançamentos', lancamentos=lancamentos, form=form, id=id,periodo=periodo)
 

# rota para editar lancamento do funcionario no banco de dados
@app.route('/editarLancamento/<int:lancamento><int:id><int:periodo>', methods = ['GET', 'POST'])
def editarLancamento(lancamento,id,periodo):
    lancamentoFuncionario = tb_periodofuncionario.query.filter_by(cod_periodoFuncionario=lancamento).first()   
    form = FormularioLancamentoEdicao()
    form.tipolancamento.data = lancamentoFuncionario.cod_tipolancamento
    form.datalancamento.data = lancamentoFuncionario.data_periodoFuncionario
    return render_template('alterarLancamento.html', titulo='Editar Lançamento', lancamento=lancamento, id=lancamentoFuncionario.cod_usuario, periodo=periodo, form=form)      
 
 # rota para atualizar lancamento do funcionario no banco de dados
@app.route('/atualizarLancamento/<int:lancamento><int:id><int:periodo>', methods = ['GET', 'POST'])
def atualizarLancamento(lancamento,id,periodo):
    form = FormularioLancamentoEdicao()
    if form.validate_on_submit():
        lancamentoFuncionario = tb_periodofuncionario.query.filter_by(cod_periodoFuncionario=lancamento).first()
        if lancamentoFuncionario:
            lancamentoFuncionario.cod_tipolancamento = form.tipolancamento.data
            id = lancamentoFuncionario.cod_usuario
            db.session.add(lancamentoFuncionario)
            db.session.commit()

    return redirect(url_for('visualizarLancamentoFuncionario', lancamento=lancamento,id=id,periodo=periodo))  
 

#---------------------------------------------------------------------------------------------------------------------------------
#RELATÓRIOS
#---------------------------------------------------------------------------------------------------------------------------------

# rota index para mostrar os usuários
@app.route('/relatorioPeriodo')
def relatorioPeriodo():
    form = FormularioPesquisaPeriodo()
    return render_template('relatorioPeriodo.html', titulo='Relatório por período', form=form)