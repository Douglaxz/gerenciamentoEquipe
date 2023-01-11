import os
from gerenciador import app

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'foto{id}.jpg' == nome_arquivo:
            return nome_arquivo
    return 'semfoto.png'