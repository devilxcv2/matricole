import json
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv
from datetime import datetime
import mysql.connector
import webbrowser
webbrowser.open("http://127.0.0.1:5000")
app = Flask(__name__)
now = datetime.now()
patch='C:\\Users\\enrico\\Documents\\matricole2\\matricole.db'

def recupera_codici():
    conn = sqlite3.connect(patch)
    c = conn.cursor()
    c.execute("SELECT codice FROM quadri")
    codici = [row[0] for row in c.fetchall()]
    conn.close()
    return codici



@app.route('/')
def home():
    data_quadri = recupera_codici()
    return render_template("index.html", data_quadri=data_quadri)
def index():
    now = datetime.now()
    context = {'now': now}
    data_quadri = recupera_codici()
    for codice in data_quadri:
        print(codice)
        
    return render_template('index.html', data_quadri=data_quadri,now=now)
    




@app.route('/esporta_csv', methods=['POST'])
def esporta_csv():
    # Connettersi al database e recuperare i dati
    with sqlite3.connect(patch) as conn:
        c = conn.cursor()
        c.execute("SELECT quantità,codice,matr_iniziale,matr_finale,data FROM matricole")
        matricole = c.fetchall()

    date1 = datetime.now().strftime("%Y")
    file_name = 'matricole_' + date1 + '.csv'
    
    # Scrivere i dati in un file CSV
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Quantità', 'Codice', 'Matricola iniziale', 'Matricola finale', 'Data'])
        for row in matricole:
            writer.writerow(row)

    # Scaricare il file esportato
    return redirect('/', code=302)

@app.route('/importa_csv', methods=['POST'])
def importa_csv():
    # Caricare il file CSV da importare
    file = request.files.get('file')
    if not file:
        return redirect('/')
    
    # Verificare che il file abbia l'estensione .csv
    filename = file.filename
    if not filename.endswith('.csv'):
        return redirect('/')

    # Connettersi al database
    with sqlite3.connect(patch) as conn:
        c = conn.cursor()

        # Creare la tabella nel database se non esiste
        c.execute("""
            CREATE TABLE IF NOT EXISTS matricole (
                quantità INTEGER,
                codice TEXT,
                matr_iniziale TEXT,
                matr_finale TEXT,
                data TEXT
            )
        """)

        # Leggere i dati dal file CSV e inserirli nel database
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            c.execute("""
                INSERT INTO matricole (quantità, codice, matr_iniziale, matr_finale, data)
                VALUES (?, ?, ?, ?, ?)
            """, row)

        # Salvare le modifiche nel database
        conn.commit()

    # Redirect alla pagina principale
    return redirect('/', code=302)




    
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
    return redirect('index.html')
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
    with sqlite3.connect(patch) as conn:
        c = conn.cursor()
        c.execute("SELECT codice FROM quadri")
        codici = [row[0] for row in c.fetchall()]
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



@app.route('/inserisci', methods=['POST'])
def inserisci():
    quantita = request.form['quantita']
    codice = request.form['codice']
    data = request.form['data']
    
    conn = sqlite3.connect(patch)
    c = conn.cursor()

    # ottieni la matricola finale più alta
    c.execute("SELECT MAX(matr_finale) FROM matricole")
    max_matr_finale = c.fetchone()[0]

    # calcola la matricola iniziale come matricola finale + 1
    matr_iniziale = max_matr_finale + 1 if max_matr_finale else 1
    matr_finale = matr_iniziale + int(quantita) - 1

    # inserisci il nuovo record
    c.execute("INSERT INTO matricole (quantità, codice, matr_iniziale, matr_finale, data) VALUES (?, ?, ?, ?, ?)", (quantita, codice, matr_iniziale, matr_finale, data))

    # salva i cambiamenti nel database
    conn.commit()

    # chiudi la connessione al database
    conn.close()

    # restituisci il valore della matricola iniziale insieme ad altri valori
   
    context = {
        'matr_iniziale': matr_iniziale,
        'quadri': recupera_codici()
    }
    return render_template('index.html', **context)
    


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