import psycopg2
from flask import Flask, jsonify, request

conexaoBD = psycopg2.connect(database = "estoqueBD",
                             host     = "localhost",
                             user     = "postgres",
                             password = "1234",
                             port     = "5432"   
                            )
cursor = conexaoBD.cursor()
app = Flask(__name__)

#Tabela produtos

# Criar
@app.route('/produtos', methods=["POST"])
def criarProduto():
    nome = request.get_json()["nome"] # Os dados que serão alterados estarão nessa requisição, o cliente informará no body do link
    qtd = request.get_json()["qtd"]
    
    cursor.execute(f"""
                        INSERT INTO produtos(nome, qtd) VALUES ('{nome}', {qtd});
                   """)
    conexaoBD.commit() # Efetiva a alteração acima no BD
    return 'Operação completa'

# Ler

# Ler todos
@app.route('/produtos', methods=['GET'])
def lerTodosProdutos():
    cursor.execute("SELECT * FROM produtos;")
    data = cursor.fetchall()
    return data

# Ler por código do produto
@app.route('/produtos/<int:cod>', methods=['GET'])
def LerProdutoID(cod):
    cursor.execute(f"SELECT * FROM produtos WHERE cod = {cod};")
    data = cursor.fetchall()
    return data

# Modificar produto
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

@app.route('/usuario/login', methods=['POST'])
def login():
    nome = request.get_json()["nome"]
    senha = request.get_json()["senha"]
    
    if verificaUsuario(nome) == 1:
        cursor.execute(f"""
                            SELECT usr_senha FROM usuarios WHERE usr_nome = '{nome}' 
                       """)
        data = cursor.fetchall()[0][0]
        
        if data == senha:
            return "Logado."
        else:
            return "Senha incorreta"
        
    else:
        return "Usuário não encontrado."
    
app.run(port=5000, host='localhost', debug=True)