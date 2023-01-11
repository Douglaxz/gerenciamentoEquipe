from gerenciador import db

# criação da classe usuário conectada com o banco de dados mysql
class usuarios(db.Model):
    cod_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(50), nullable=False)
    senha_usuario = db.Column(db.String(50), nullable=False)
    status_usuario = db.Column(db.Integer, nullable=False)
    login_usuario = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name