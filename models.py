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
    
class resultadoBusca:
    def __init__(self, nome, situacao, d1, d2, d3 ,d4 , d5, d6 , d7, d8, d9, d10, d11, d12, d13 , d14 , d15, d16 , d17, d18, d19, d20, d21, d22, d23 ,d24 , d25, d26 , d27, d28, d29, d30, d31):
        self.nome = nome
        self.situacao = situacao
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.d4 = d4
        self.d5 = d5
        self.d6 = d6
        self.d7 = d7
        self.d8 = d8        
        self.d9 = d9
        self.d10 = d10
        self.d11 = d11
        self.d12 = d12
        self.d13 = d13
        self.d14 = d14
        self.d15 = d15
        self.d16 = d16
        self.d17 = d17
        self.d18 = d18        
        self.d19 = d19
        self.d20 = d20     
        self.d21 = d21
        self.d22 = d22
        self.d23 = d23
        self.d24 = d24
        self.d25 = d25
        self.d26 = d26
        self.d27 = d27
        self.d28 = d28        
        self.d29 = d29
        self.d30 = d30           
