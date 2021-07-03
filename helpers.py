import os
import time
from flask import request
from jogoteca import app


def recupera_imagem(id):
    for nome_arquivo in os.listdir((app.config['UPLOAD_PATH'])):
        if f'capa{id}' in nome_arquivo: #if capa{id} contains(capa) retorna capa
            return nome_arquivo

def atualiza_capa(id):
    timestamp = time.time()
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    imagem_deletar = recupera_imagem(id)
    if imagem_deletar in os.listdir(upload_path):
        os.remove(os.path.join(upload_path, imagem_deletar))
    arquivo.save(f'{upload_path}/capa{id}-{timestamp}.jpg')


def deleta_imagem(id):
    imagem = recupera_imagem(id)
    upload_path = app.config['UPLOAD_PATH']
    if imagem is not None:
        os.remove(os.path.join(upload_path, imagem))