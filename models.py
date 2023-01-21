from gerenciador import db


# criação da classe usuário conectada com o banco de dados mysql
class tb_usuarios(db.Model):
    cod_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(50), nullable=False)
    senha_usuario = db.Column(db.String(50), nullable=False)
    status_usuario = db.Column(db.Integer, nullable=False)
    login_usuario = db.Column(db.String(50), nullable=False)
    cod_tipousuario = db.Column(db.Integer, nullable=False)
    cod_area = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

# criação da classe tipousuário conectada com o banco de dados mysql
class tb_tipousuario(db.Model):
    cod_tipousuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_tipousuario = db.Column(db.String(50), nullable=False)
    status_tipousuario = db.Column(db.Integer, nullable=False)

# criação da classe beneficios conectada com o banco de dados mysql
class tb_beneficios(db.Model):
    cod_beneficio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_beneficio = db.Column(db.String(50), nullable=False)
    status_beneficio = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name        

# criação da classe area conectada com o banco de dados mysql
class tb_areas(db.Model):
    cod_area = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_area = db.Column(db.String(50), nullable=False)
    status_area = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name   

# criação da classe tipo lancamento conectada com o banco de dados mysql
class tb_tipolancamento(db.Model):
    cod_tipolancamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_tipolancamento = db.Column(db.String(50), nullable=False)
    status_tipolancamento = db.Column(db.Integer, nullable=False)
    sigla_tipolancamento = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

# criação da classe beneficio usuario conectada com o banco de dados mysql
class tb_beneficiousuario(db.Model):
    cod_beneficiousuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_usuario = db.Column(db.Integer, nullable=False)
    cod_beneficio = db.Column(db.Integer, nullable=False)

# criação da classe periodoconectada com o banco de dados mysql    
class tb_periodos(db.Model):
    cod_periodo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_periodo = db.Column(db.String(50), nullable=False)
    status_periodo = db.Column(db.Integer, nullable=False)
    inicio_periodo = db.Column(db.DateTime, nullable=False)
    final_periodo = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name     

# criação da classe periodoconectada com o banco de dados mysql    
class tb_periodofuncionario(db.Model):
    cod_periodoFuncionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_usuario = db.Column(db.Integer, nullable=False)
    cod_periodo = db.Column(db.Integer, nullable=False)
    cod_tipolancamento = db.Column(db.Integer, nullable=False)
    data_periodoFuncionario = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name    
    
#class resultadoBusca:
#    def __init__(self, nome, situacao, 1, 2, 3 ,4 , 5, 6 , 7, 8, 9, 10, 11, 12, 13 , 14 , 15, 16 , 17, 18, 19, 20, 21, 22, 23 ,24 , 25, 26 , 27, 28, 29, 30, 31):
#        self.nome = nome
#        self.situacao = situacao
#        self.1 = 1