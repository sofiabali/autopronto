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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            marca TEXT NOT NULL,
            ano INTEGER,
            valor_diaria REAL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/carros')
def carros():
    conn = conectar_bd()
    carros = conn.execute('SELECT * FROM veiculos').fetchall()
    conn.close()
    return render_template('carros.html', carros=carros)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        ano = request.form['ano']
        valor_diaria = request.form['valor_diaria']

        conn = conectar_bd()
        conn.execute('INSERT INTO veiculos (modelo, marca, ano, valor_diaria) VALUES (?, ?, ?, ?)',
                     (modelo, marca, ano, valor_diaria))
        conn.commit()
        conn.close()
        return redirect(url_for('carros'))
    return render_template('cadastro.html')

# ---- API para JS (exemplo AJAX) ----
@app.route('/api/carros')
def api_carros():
    conn = conectar_bd()
    carros = conn.execute('SELECT * FROM veiculos').fetchall()
    conn.close()
    return jsonify([dict(c) for c in carros])

if __name__ == '__main__':
    criar_tabelas()
    app.run(debug=True)