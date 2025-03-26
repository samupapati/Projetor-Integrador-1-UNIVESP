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
                        INSERT INTO produtos(nome, qtd) VALUES ('{nome}', {qtd})
                   """)
    conexaoBD.commit() # Efetiva a alteração acima no BD
    return 'Operação completa'
