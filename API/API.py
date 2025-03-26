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

cursor.execute("CREATE TABLE teste(id INTEGER PRIMARY KEY);")
cursor.execute('INSERT INTO teste(id) VALUES (1);')
conexaoBD.commit()
cursor.execute("SELECT * FROM teste;")
print(cursor.fetchall())

# #Criar
# @app.route('/produtos', methods=["POST"])
# def criarProduto(cod, nome, qtd):
    