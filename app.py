from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

#index
@app.route('/')
def index():
    return render_template('index.html')

def dashboard():
    dashboard = request.args.get("dashboard") == "1"
    return dict(dashboar=dashboard)

#login
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_autenticacao', methods=['POST'])
def login_autenticacao():
    matricula = request.form['user']
    senha = request.form['pin']
    usuarios = "usuarios.json"
    arquivo = open(usuarios, 'r', encoding='utf-8')
    dados = json.load(arquivo)
    arquivo.close()
    for usuario in dados:
        if usuario['user'] == matricula and usuario['senha'] == senha:
            funcao = usuario['funcao']
            return redirect(f'/{funcao}?user={usuario["user"]}')
        
    return render_template('cadastro.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastro.html')

#cadastro
@app.route('/cadastro', methods=['post'])
def cadastro():
    user = request.form['user']
    senha = request.form['pin']
    funcao = request.form['funcao'] 
    email= request.form['email'] 
    telefone= request.form['telefone'] 

    usuarios = "usuarios.json"

    arquivo = open(usuarios, 'r', encoding='utf-8')
    dados = json.load(arquivo)
    arquivo.close()

    novo_usuario = {
        'user': user,
        'funcao': funcao,
        'senha': senha,
        'telefone': telefone,
         'email': email,
    }

    dados.append(novo_usuario)

    arquivo = open(usuarios, 'w', encoding='utf-8')
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    arquivo.close()

    return redirect(f'/{funcao}?user==user')

def carregar_usuarios():
    with open('usuarios.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def pesquisa(termo):
    termo = termo.lower() 
    usuarios = carregar_usuarios()
    if termo:
        return [u for u in usuarios if termo in u['funcao'].lower()]
    else:
        return []
    
#servidor
@app.route('/servidor')
def servidor():
    usuario = request.args.get('user') 
    query = request.args.get('q', '')
    resultados = pesquisa(query)
    return render_template('servidor.html', usuario=usuario, resultados=resultados)

#tutor
@app.route('/tutor')
def tutor():
    return render_template('tutor.html')

#tutorado
@app.route('/tutorado')
def tutorado():
    return render_template('tutorado.html')

#professor
@app.route('/professor')
def professor():
    return render_template('professor.html')

#professor_orientador
@app.route('/professor_orientador')
def professor_orientador():
    return render_template('professor_orientador.html')

#sessao_tutoria
@app.route('/sessao_tutoria')
def sessao_tutoria():
    return render_template('sessao_tutoria.html')



if __name__ == '__main__':
    app.run()