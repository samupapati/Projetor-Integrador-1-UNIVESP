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

# Criar
@app.route('/produtos', methods=["POST"])
def criarProduto(nome, qtd):
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
    data = request.get_json() # Os dados que serão alterados estarão nessa requisição, o cliente informará no body do link
    cursor.execute(f"""
                        UPDATE produtos SET nome = '{data['nome']}' WHERE cod = {cod};
                        UPDATE produtos SET qtd = {data['qtd']} WHERE cod = {cod};
                   """)
    conexaoBD.commit()
    return "Operação completa"

# Excluir produto
@app.route('/produtos/<int:cod>', methods=['DELETE'])
def excluirProduto(cod):
    cursor.execute(f"DELETE FROM produtos WHERE cod = {cod}")
    conexaoBD.commit()
    return "Operação completa"
    
app.run(port=5000, host='localhost', debug=True)