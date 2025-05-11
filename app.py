import psycopg2, os
from flask import Flask, jsonify, request, send_from_directory
port = int(os.environ.get('PORT', 5000))
DATABASE_URL = os.environ.get('DATABASE_URL')

# Tabela produtos
conexaoBD = psycopg2.connect(database = DATABASE_URL, sslmode  = "require")
cursor = conexaoBD.cursor()

app = Flask(__name__, static_folder='static', template_folder='templates')


# Rota para a página principal
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

# Rota para a página de dashboard
@app.route('/dashboard')
def dashboard():
    return send_from_directory('templates', 'dashboard.html')

# Inserir produto
@app.route('/produtos', methods=["POST"])
def criarProduto():
    nome = request.get_json()["nome"] # Os dados que serão alterados estarão nessa requisição, o cliente informará no body do link
    qtd = request.get_json()["qtd"]
    
    cursor.execute(f"""
                        INSERT INTO produtos(nome, qtd) VALUES ('{nome}', {qtd});
                   """)
    conexaoBD.commit() # Efetiva a alteração acima no BD
    return 'Operação completa'

# Listar todos os produtos
@app.route('/produtos', methods=['GET'])
def lerTodosProdutos():
    cursor.execute("SELECT * FROM produtos;")
    data = cursor.fetchall()
    return data

# Listar por código do produto
@app.route('/produtos/<int:cod>', methods=['GET'])
def LerProdutoID(cod):
    cursor.execute(f"SELECT * FROM produtos WHERE cod = {cod};")
    data = cursor.fetchall()
    return data

# Editar produto
@app.route('/produtos/<int:cod>', methods=["PUT"])
def modificarProduto(cod):
    nome = request.get_json()["nome"]
    qtd = request.get_json()["qtd"]
    
    cursor.execute(f"""
                        UPDATE produtos SET nome = '{nome}' WHERE cod = {cod};
                        UPDATE produtos SET qtd = {qtd} WHERE cod = {cod};
                   """)
    conexaoBD.commit()
    return "Operação completa"

# Excluir produto
@app.route('/produtos/<int:cod>', methods=['DELETE'])
def excluirProduto(cod):
    cursor.execute(f"DELETE FROM produtos WHERE cod = {cod}")
    conexaoBD.commit()
    return "Operação completa"


#Tabela usuarios
def verificaUsuario(nome):
    cursor.execute(f"""
                        SELECT COUNT(*) AS COUNT FROM usuarios WHERE usr_nome = '{nome}' 
                   """)
    data = cursor.fetchall()

    return data[0][0] # Sem os zeros retornará dessa forma: [()] Primeiro zero: acessa a primeira tupla, segundo zero acessa o número

@app.route('/usuario', methods=['POST'])
def criarUsuario():
    nome = request.get_json()["nome"]
    senha = request.get_json()["senha"]
    
    if verificaUsuario(nome) == 1:
        return "Usuário já criado."
    else:
        cursor.execute(f"""
                            INSERT INTO usuarios(usr_nome, usr_senha) VALUES ('{nome}', '{senha}');
                       """)
        conexaoBD.commit()
        return "Usuário criado com sucesso."

@app.route('/login', methods=['POST'])
def login():
    nome = request.get_json()["nome"]
    senha = request.get_json()["senha"]
    
    if verificaUsuario(nome) == 1:
        cursor.execute(f"""
                            SELECT usr_senha FROM usuarios WHERE usr_nome = '{nome}' 
                       """)
        data = cursor.fetchall()[0][0]
        
        if data == senha:
            return jsonify({"message": "Logado", "redirect": "/dashboard"}), 200  # Retorna a mensagem e o redirecionamento
        else:
            return jsonify({"message": "Senha incorreta"}), 401  # Retorna erro com status 401
        
    else:
        return jsonify({"message": "Usuario nao encontrado."}), 404  # Retorna erro com status 404'

app.run(port=port, host='0.0.0.0', debug=True)