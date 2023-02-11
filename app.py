import json
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    data_quadri = recupera_codici()
    return render_template('/index.html', data_quadri=data_quadri)

def recupera_codici():
    conn = sqlite3.connect('C:\\Users\\enrico\\Documents\\pythoncode\\mio\\matricole.db')
    c = conn.cursor()
    c.execute("SELECT codice FROM quadri")
    codici = [row[0] for row in c.fetchall()]
    conn.close()
    return codici


@app.route('/inserisci', methods=['POST'])
def inserisci():
    quantita = request.form['quantita']
    codice = request.form['codice']
    matr_iniziale = request.form['matr_iniziale']
    matr_finale = request.form['matr_finale']
    data = request.form['data']
    
    conn = sqlite3.connect('C:\\Users\\enrico\\Documents\\pythoncode\\mio\\matricole.db')
    c = conn.cursor()
    c.execute("INSERT INTO matricole (quantità, codice, matr_iniziale, matr_finale, data) VALUES (?, ?, ?, ?, ?)", (quantita, codice, matr_iniziale, matr_finale, data))
    conn.commit()
    conn.close()
    #return redirect('/')
    #return 'Dati inseriti con successo!'
    
@app.route('/codici')
def codici():
    conn = sqlite3.connect('C:\\Users\\enrico\\Documents\\pythoncode\\mio\\matricole.db')
    c = conn.cursor()
    c.execute("SELECT codice FROM quadri")
    codici = [row[0] for row in c.fetchall()]
    conn.close()

    return codici

@app.route('/aggiorna', methods=['POST'])
def aggiorna():
    quantita = request.form['quantita']
    codice = request.form['codice']
    matr_iniziale = request.form['matr_iniziale']
    matr_finale = request.form['matr_finale']
    data = request.form['data']
    
    conn = sqlite3.connect(patch)
    c = conn.cursor()
    c.execute("INSERT INTO matricole (quantità, codice, matr_iniziale, matr_finale, data) VALUES (?, ?, ?, ?, ?)", (quantita, codice, matr_iniziale, matr_finale, data))
    conn.commit()
    conn.close()
    return redirect('/')
    #return 'Dati aggiornati con successo!'


@app.route('/visualizza_matricole')
def visualizza_matricole():
    conn = sqlite3.connect('C:\\Users\\enrico\\Documents\\pythoncode\\mio\\matricole.db')
    c = conn.cursor()
    c.execute("SELECT * FROM matricole")
    matricole = c.fetchall()
    conn.close()
    return render_template('matricole.html', matricole=matricole)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

