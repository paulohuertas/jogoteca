from flask import render_template, request, redirect, flash, session, url_for, send_from_directory
from models import Jogo, Usuario
from dao import JogoDao, UsuarioDao
from helpers import deleta_imagem, atualiza_capa, recupera_imagem
from jogoteca import db, app
import time

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

#criando a roda index. render_template ira renderizar a pagina passando as seguintes informacoes:
#renderize a pagina: lista.html, titulo = jogo, passando uma lista de jogos. URL = endereco esta sendo usado
#na tag <p>
@app.route('/')
def index():
    list_of_games = jogo_dao.listar()
    return render_template('lista.html', titulo="Jogo", jogos=list_of_games,
                           categoria="Categoria", console="Console")


#criando a rota novo. Ira renderizar o novo.html
@app.route('/novo', methods=['POST', 'GET'])
def novo():
        if 'usuario_logado' not in session or session['usuario_logado'] == None:
            return redirect(url_for('login', proxima=url_for('novo')))
        return render_template('novo.html', titulo="Novo Jogo")


@app.route('/registrar', methods=['POST', 'GET'])
def registrar():
    if session['usuario_logado']:
        return redirect(url_for('index'))
    return render_template('registrar.html', titulo="Registrar novo usaurio")

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    id = request.form['id']
    nome = request.form['nome']
    senha = request.form['senha']
    usuario = Usuario(id, nome, senha)
    usuario_existe = usuario_dao.buscar_por_id(id)
    if usuario_existe is None or usuario_existe.id != usuario.id:
        usuario_dao.salvar(usuario)
        flash("Registro efetuado com sucesso", "success")
        return redirect(url_for('login'))
    else:
        flash("Usuario ja cadastrado", "danger")
        return redirect(url_for('registrar'))


#criando a rota criar. Ela ira renderizar a lista de jogos criados.
#request eh uma funcao do flask que acessa o formulario e tambem o dicionario das informacoes que estao sendo passada
#atraves do form. Por isso -> request.form['nome']. ['nome'] esta sendo passado atraves da tag input
#<input type="text" id="no  me" name="nome" class="form-control">
@app.route('/criar', methods=['POST', 'GET'])
def criar():
    #pegamos informacoes do form atraves do request
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    #criamos uma instancia de jogo
    jogo = Jogo(nome, categoria, console)
    #salvamos no banco de dados
    jogo_dao.salvar(jogo)
    #pegamos informacoes do arquivo/file
    #atualiza_capa(jogo.id)
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    nome_capa = f'capa{jogo.id}-{timestamp}.jpg'
    arquivo.save(f'{upload_path}/{nome_capa}')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar(id):
        if 'usuario_logado' not in session or session['usuario_logado'] == None:
            return redirect(url_for('login', proxima=url_for('editar', id=id)))
        jogo = jogo_dao.busca_por_id(id)
        nome_imagem = recupera_imagem(id)
        print(nome_imagem)
        return render_template('editar.html', titulo="Editando Jogo", jogo=jogo, capa_jogo=nome_imagem)


@app.route('/atualizar', methods=['POST'])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    id = request.form['id']
    jogo = Jogo(nome, categoria, console, id)
    jogo_dao.salvar(jogo)

    atualiza_capa(id)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('delete', id=id)))
    jogo = jogo_dao.busca_por_id(id)
    nome_arquivo = recupera_imagem(id)
    return render_template('deletar.html', titulo="Deletar jogo", jogo=jogo, nome_arquivo=nome_arquivo)

@app.route('/apagar', methods=['POST'])
def apagar():
    id = request.form['id']
    exist = jogo_dao.busca_por_id(id)
    if exist:
        jogo_dao.deletar(id)
        flash("Jogo removido com sucesso!", "success")
        deleta_imagem(id)
        return redirect(url_for('index'))
    else:
        flash("Unable to find id", "alert")
        return redirect(url_for('index'))


#/login?proxima=novo
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo="Login", proxima=proxima)


@app.route('/autenticar', methods=['POST'],)
def autenticar():
    usuario = usuario_dao.buscar_por_id([request.form['usuario']])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id

            proxima_pagina = request.form['proxima']
            flash(usuario.nome + ", voce logou com sucesso!", "success")
            return redirect(proxima_pagina)
        else:
            flash("Usuario ou senha invalido. Tente novamente!", "danger")
            return redirect(url_for('login'))
    else:
        flash("Usuario nao existe. Tente registrar primeiro")
        return redirect(url_for('registrar'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Usuario deslogado com sucesso!", "success")
    return redirect(url_for('index'))

#nome_arquivo vem atraves do formulario editar
@app.route('/imagem/<nome_arquivo>')
def imagem(nome_arquivo):
    #send_from_directory busca na pasta uploads o nome do arquivo
     return send_from_directory('uploads', nome_arquivo)

#form action="/criar" method="Post". Eh como se o formulario envelopasse as informacoes do formulario
#criasse um dicionario de dados e passasse essas informacoes atraves do metodo "Post". Esse metodo e action
#levara essas informacoes para a action com o mesmo nome no arquivo de rotas.