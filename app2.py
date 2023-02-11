import json
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import mysql.connector
import webbrowser
webbrowser.open("http://127.0.0.1:5000")
app = Flask(__name__)

patch='C:\\Users\\User\\Documents\\matricole\\matricole.db'
@app.route('/')
def index():
    data_quadri = recupera_codici()
    return render_template('index.html', data_quadri=data_quadri, now=datetime.now())

def recupera_codici():
    conn = sqlite3.connect(patch)
    c = conn.cursor()
    c.execute("SELECT codice FROM quadri")
    codici = [row[0] for row in c.fetchall()]
    conn.close()
    return codici


@app.route('/inserisci', methods=['POST'])
def inserisci():
    quantita = request.form['quantita']
    codice = request.form['codice']
    matr_finale = request.form['matr_finale']
    data = request.form['data']
    
    # calcola la matr_iniziale come matr_finale + 1
    matr_iniziale = int(matr_finale) + 1
    
    conn = sqlite3.connect(patch)
    c = conn.cursor()
    c.execute("INSERT INTO matricole (quantità, codice, matr_iniziale, matr_finale, data) VALUES (?, ?, ?, ?, ?)", (quantita, codice, matr_iniziale, matr_finale, data))
    conn.commit()
    conn.close()
    return redirect('/')
    #return 'Dati inseriti con successo!'

    
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

@app.route('/modifica', methods=['GET', 'POST'])
def modifica():
    conn = sqlite3.connect(patch)
    c = conn.cursor()
    c.execute("SELECT * FROM matricole")
    dati = c.fetchall()
    conn.close()
    
    if request.method == 'POST':
        quantita = request.form['quantita']
        codice = request.form['codice']
        matr_iniziale = request.form['matr_iniziale']
        matr_finale = request.form['matr_finale']
        data = request.form['data']
        
        conn = sqlite3.connect(patch)
        c = conn.cursor()
        c.execute("UPDATE matricole SET quantità=?, codice=?, matr_iniziale=?, matr_finale=? WHERE data=?", (quantita, codice, matr_iniziale, matr_finale, data))
        conn.commit()
        conn.close()
        return redirect('/')
        
    return render_template('modifica.html', dati=dati)





@app.route('/codici')
def codici():
    conn = sqlite3.connect(patch)
    c = conn.cursor()
    c.execute("SELECT codice FROM quadri")
    codici = [row[0] for row in c.fetchall()]
    conn.close()
    return codici




@app.route('/matricole')
def visualizza_matricole():
    conn = sqlite3.connect(patch)
    c = conn.cursor()
    c.execute("SELECT quantità,codice,matr_iniziale,matr_finale, data FROM matricole")
    matricole = c.fetchall()
    conn.close()
    return render_template('matricole.html', matricole=matricole)

@app.route('/quadri')
def visualizza_quadri():
    conn = sqlite3.connect(patch)
    c = conn.cursor()
    c.execute("SELECT id,codice FROM quadri")
    quadri = c.fetchall()
    conn.close()
    return render_template('quadri.html', quadri=quadri)



@app.route('/inserisci_quadro', methods=['POST'])
def inserisci_quadro():
    if 'codice' in request.form:
        codice = request.form['codice']
        conn = sqlite3.connect(patch)
        c = conn.cursor()

        # inserisci il nuovo quadro
        c.execute("INSERT INTO quadri (codice) VALUES (?)", (codice,))

        # salva i cambiamenti nel database
        conn.commit()

        # chiudi la connessione al database
        conn.close()
        return redirect('/')
        #return 'Dati inseriti con successo!'
    else:
        return 'Nessun codice inviato.'


@app.route('/cerca_quadro', methods=['POST'])
def cerca_quadro():
    if 'codice' in request.form:
        codice = request.form['codice']
        conn = sqlite3.connect(patch)
        c = conn.cursor()

        c.execute("SELECT * FROM quadri WHERE codice LIKE ?", ('%'+codice+'%',))
        quadro = c.fetchone()
        if quadro:
            return 'Il quadro è stato trovato con codice: {} e i seguenti dettagli: {}'.format(quadro[0], quadro)
        else:
            return 'Il quadro non è stato trovato.'
        
        conn.close()
    else:
        return 'Nessun codice inviato.'


@app.route('/cerca_matricola', methods=['POST'])
def cerca_matricola():
    if 'codice' in request.form:
        codice = request.form['codice']
        conn = sqlite3.connect(patch)
        c = conn.cursor()

        c.execute("SELECT *  FROM matricole WHERE codice LIKE ?", ('%'+codice+'%',))
        matricole = c.fetchall()
        if matricole:
            sum_quantity = sum(int(x[1]) for x in matricole)

            return render_template('matricole_ricerca.html', matricole=matricole, sum_quantity=sum_quantity)
        else:
            return 'Nessuna matricola associata al codice {} trovata.'.format(codice)
        
        conn.close()
    else:
        return 'Nessun codice di matricola inviato.'

@app.route('/delete_record', methods=['POST'])
def delete_record():
    id = request.form.get('record_id')
    print("ID record da eliminare:", id)
    if not id:
        return "Record ID non presente"
    try:
        conn = sqlite3.connect((patch))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM matricole WHERE id=?", (id,))
        conn.commit()
        message = "Record eliminato con successo"
    except Exception as e:
        return str(e)
    finally:
        conn.close()
    return redirect(url_for('modifica'))




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)