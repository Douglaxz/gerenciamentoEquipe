from gerenciador import db


# criação da classe usuário conectada com o banco de dados mysql
class tb_usuarios(db.Model):
    cod_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(50), nullable=False)
    senha_usuario = db.Column(db.String(50), nullable=False)
    status_usuario = db.Column(db.Integer, nullable=False)
    login_usuario = db.Column(db.String(50), nullable=False)
    cod_tipousuario = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

# criação da classe tipousuário conectada com o banco de dados mysql
class tb_tipousuario(db.Model):
    cod_tipousuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_tipousuario = db.Column(db.String(50), nullable=False)
    status_tipousuario = db.Column(db.Integer, nullable=False)

# criação da classe usuário conectada com o banco de dados mysql
class tb_beneficios(db.Model):
    cod_beneficio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_beneficio = db.Column(db.String(50), nullable=False)
    status_beneficio = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name        

# criação da classe usuário conectada com o banco de dados mysql
class tb_areas(db.Model):
    cod_area = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_area = db.Column(db.String(50), nullable=False)
    status_area = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name        
          