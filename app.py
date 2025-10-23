from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)


def conectar_bd():
    conn = sqlite3.connect('locadora.db')
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = conectar_bd()
    cursor = conn.cursor()

    # tabela de veículos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            marca TEXT NOT NULL,
            ano INTEGER,
            valor_diaria REAL
        )
    ''')

    # tabela de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT,
            cpf TEXT UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# cria as tabelas ao iniciar o servidor
criar_tabelas()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/carros')
def carros():
    conn = conectar_bd()
    carros = conn.execute('SELECT * FROM veiculos').fetchall()
    conn.close()
    return render_template('carros.html', carros=carros)


@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        senha = request.form['senha']

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, email, telefone, cpf, senha)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, telefone, cpf, senha))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('cadastro_cliente.html')


@app.route('/adicionar_carro', methods=['POST'])
def adicionar_carro():
    data = request.get_json()
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO veiculos (modelo, marca, ano, valor_diaria)
        VALUES (?, ?, ?, ?)
    ''', (data['modelo'], data['marca'], data['ano'], data['valor_diaria']))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Carro adicionado com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)

