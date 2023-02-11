
import sqlite3
from tkinter import messagebox
import tkinter
import texttable as tt
import pandas as pd
from tkinter import *
import tkinter.filedialog as filedialog
from datetime import datetime
import pyreadline
from tkinter import ttk
from tkinter import Tk, Label
from tkinter.ttk import Scrollbar
from tkinter import *

import webbrowser
import pandas as pd
tabella_text_box = None
patch='C:\\Users\\User\\Documents\\matricole\\matricole.db'
def stampa_tabella_matricole_html():
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()
    cursor.execute("SELECT quantità, codice, matr_iniziale, matr_finale, data FROM matricole")
    rows = cursor.fetchall()
    
    # Crea un DataFrame dai dati della tabella matricole
    df = pd.DataFrame(rows, columns=['quantità', 'codice', 'matr_iniziale', 'matr_finale', 'data'])
    
    # Genera il codice HTML per la tabella matricole
    html_tabella = df.to_html()
    
    # Stampa o salva il codice HTML generato
    print(html_tabella)
    # o
    with open('tabella_matricole.html', 'w') as f:
        f.write(html_tabella)
    
    
    conn.close()

def stampa_tabella_quadri_html():
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quadri")
    rows = cursor.fetchall()
    
    # Crea un DataFrame dai dati della tabella matricole
    df = pd.DataFrame(rows, columns=['id', 'codice'])
    
    # Genera il codice HTML per la tabella matricole
    html_tabella_quadri = df.to_html()
    
    # Salva il codice HTML generato in un file
    with open('tabella_quadri.html', 'w') as f:
        f.write(html_tabella_quadri)
    
    # Apre il file HTML appena creato nel browser predefinito
    webbrowser.open_new_tab('tabella_quadri.html')
    
    conn.close()
def stampa_tabella_matricole_html():
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()
    cursor.execute("SELECT quantità, codice, matr_iniziale, matr_finale, data FROM matricole")
    rows = cursor.fetchall()
    
    # Crea un DataFrame dai dati della tabella matricole
    df = pd.DataFrame(rows, columns=['quantità', 'codice', 'matr_iniziale', 'matr_finale', 'data'])
    
    # Genera il codice HTML per la tabella matricole
    html_tabella_matricole = df.to_html()
    
    # Salva il codice HTML generato in un file
    with open('tabella_matricole.html', 'w') as f:
        f.write(html_tabella_matricole)
    
    # Apre il file HTML appena creato nel browser predefinito
    webbrowser.open_new_tab('tabella_matricole.html')
    
    conn.close()


def crea_finestra_tabella():
    global tabella_text_box
    finestra_tabella = Tk()
    finestra_tabella.title("Tabella matricole")
    
    tabella_text_box = Text(finestra_tabella)
    tabella_text_box.pack()
    stampa_tabella_matricole(tabella_text_box)

    finestra_tabella.mainloop()
    
def stampa_tabella(tabella_text_box, dati):
    tab = tt.Texttable()
    tab.add_rows(dati, header=False)
    tabella_text_box.insert(END, tab.draw())

def stampa_tabella_matricole():
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()
    cursor.execute("SELECT quantità, codice, matr_iniziale, matr_finale, data FROM matricole")
    rows = cursor.fetchall()
    
    # Crea una nuova finestra per la visualizzazione della tabella
    finestra_tabella = Tk()
    finestra_tabella.title("Tabella matricole")
    
    # Crea una Text Box per visualizzare la tabella
    tabella_text_box = Text(finestra_tabella)
    tabella_text_box.pack()
    font = ('Arial', 12)
    tabella_text_box.configure(font=font)
    tabella_text_box.config(width=1280, height=1024)
    if tabella_text_box:
      # Inserisci i valori della tabella nella Text Box
      for row in rows:
        
        #for item in row:
        tabella_text_box.insert(END, str(row) + '\n')
    else:
      print("Tabella text box non esiste")
    conn.close()
    finestra_tabella.mainloop()
    
def elimina_tutti_i_record():
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matricole")
    conn.commit()
    conn.close()


def stampa_tabella_quadri():
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()
    cursor.execute("SELECT codice FROM quadri")
    rows = cursor.fetchall()
    
    # Crea una nuova finestra per la visualizzazione della tabella
    finestra_tabella = Tk()
    finestra_tabella.title("Tabella quadri")
    

    # Crea una Text Box per visualizzare la tabella
    tabella_text_box = Text(finestra_tabella)
    tabella_text_box.pack()
    font = ('Arial', 10)
    tabella_text_box.configure(font=font)
    tabella_text_box.config(width=1280, height=1024)
    if tabella_text_box:
      # Inserisci i valori della tabella nella Text Box
      for row in rows:
        
        for item in row:
            tabella_text_box.insert(END, str(item) + '\n')
    else:
      print("Tabella text box non esiste")
    conn.close()
    finestra_tabella.mainloop()



def completa_codice(event):
    # recupera il codice digitato
    codice = event.widget.get()
    # verifica se il codice esiste nella tabella "quadri"
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()
    cursor.execute("SELECT codice FROM quadri WHERE codice = ?", (codice,))
    codice_completo = cursor.fetchone()
    conn.close()
    
    # se il codice esiste, completa il codice nell'oggetto Entry
    if codice_completo:
        event.widget.delete(0, 'end')
        event.widget.insert(0, codice_completo[0])
def inserisci_dati():
    state = 0
    codice_entry.bind('<KeyRelease>', completa_codice)
    state += 1
    data_corrente = datetime.now().strftime("%d-%m-%Y ")
    data_entry.delete(0, END)
    data_entry.insert(0, data_corrente)
    # recupera i valori inseriti dagli entry widgets
    quantità = quantità_entry.get()
    codice = codice_entry.get()
    matr_iniziale = matr_iniziale_entry.get()
    matr_finale = int(matr_iniziale) + int(quantità)
    data = data_entry.get()

    # connette al database
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()

    # inserisce i dati nella tabella matricole
    cursor.execute("INSERT INTO matricole (quantità, codice, matr_iniziale, matr_finale, data) VALUES (?,?,?,?,?)", (quantità, codice, matr_iniziale, matr_finale, data))
    conn.commit()
    conn.close()
    # pulisce gli entry widgets
    codice_entry.delete(0, END)
    quantità_entry.delete(0, END)
    matr_iniziale_entry.delete(0, END)
    data_entry.delete(0, END)
    data_entry.insert(0, data_corrente)
    # visualizza un messaggio di conferma
    messagebox.showinfo("Conferma", "Dati inseriti correttamente!")
def esporta_quadri_csv():
    # connette al database
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()

    # legge i dati dalla tabella 'quadri'
    cursor.execute("SELECT * FROM quadri")
    rows = cursor.fetchall()

    # crea un DataFrame pandas a partire dai dati recuperati
    df = pd.DataFrame(rows)

    # salva il DataFrame in un file CSV
    df.to_csv('quadri.csv', index=False)

    # chiude la connessione al database
    conn.close()
    
def load_csv_into_table(file_name):
    import csv

    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        table_data = []
        for row in csv_reader:
            table_data.append(row)

        return table_data

def importa_dati_da_xlsx():
    # chiede all'utente di selezionare il file xlsx da importare
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.csv")])
    
    # legge i dati dal file xlsx
    data = pd.read_csv(filepath)
     # connette al database
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()

    # inserisce i dati nella tabella quadri
    data.to_sql('quadri', conn, if_exists='replace', index=False)
    # salva le modifiche e chiude la connessione
    conn.commit()
    conn.close()
def stampa_tabella_matricole1():
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matricole")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    if tkinter.messagebox.askyesno("Ritornare alla pagina iniziale?", "Vuoi tornare alla pagina iniziale di inserimento?"):
    # inserisci qui il codice per tornare alla pagina iniziale
        root.mainloop()
    else:
        # inserisci qui il codice per uscire dall'applicazione
        pass
    conn.close()
    


def stampa_tabella():
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quadri")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def cerca_codice():
    global codice_entry
    codice = codice_entry.get()
    conn = sqlite3.connect(patch)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matricole WHERE codice = ?", (codice,))
    risultato = cursor.fetchone()
    if risultato:
        print("Il codice {} esiste nella tabella matricole".format(codice))
    else:
        print("Il codice {} non esiste nella tabella matricole".format(codice))
    conn.close()
    codice_entry.bind("<Return>", cerca_codice)
# crea la finestra principale


root = Tk()

codice_entry = Entry(root)
codice_entry.bind("<KeyPress>",lambda event: completa_codice(codice_entry.get(),state))

# crea gli elementi dell'interfaccia grafica
quantità_label = Label(root, text="Quantità:")
quantità_entry = Entry(root)
codice_label = Label(root, text="Codice:")
codice_entry = Entry(root)
matr_iniziale_label = Label(root, text="Matricola iniziale:")
matr_iniziale_entry = Entry(root)
matr_finale_label = Label(root, text="Matricola finale:")
matr_finale_entry = Entry(root)
data_label = Label(root, text="Data:")
data_entry = Entry(root)
inserisci_button = Button(root, text="Inserisci", command=inserisci_dati)
importa_dati_button = Button(root, text="Importa dati", command=importa_dati_da_xlsx)
esporta_quadri_button = Button(root, text="Esporta quadri", command=esporta_quadri_csv)
stampa_quadri_button = Button(root, text="stampa quadri", command=stampa_tabella_quadri)
stampa_matricole_button = Button(root, text="stampa matricole ", command=stampa_tabella_matricole)
cerca_quadri_button = Button(root, text="cerca quadri", command=cerca_codice)
stampa_matricole_html =Button(root, text="matricole html", command=stampa_tabella_matricole_html)
stampa_quadri_html =Button(root, text="quadri html", command=stampa_tabella_quadri_html)
stampa_matricole_label=Button(root, text="stampa matricole", command=stampa_tabella_matricole)

# posiziona gli elementi dell'interfaccia grafica
quantità_label.grid(row=0, column=0)
quantità_entry.grid(row=0, column=1)
codice_label.grid(row=1, column=0)
codice_entry.grid(row=1, column=1)
matr_iniziale_label.grid(row=2, column=0)
matr_iniziale_entry.grid(row=2, column=1)
matr_finale_label.grid(row=3, column=0)
matr_finale_entry.grid(row=3, column=1)
data_label.grid(row=4, column=0)
data_entry.grid(row=4, column=1)
inserisci_button.grid(row=5, column=80)
importa_dati_button.grid(row=8, column=80)
esporta_quadri_button.grid(row=7, column=80)
stampa_quadri_button.grid(row=9, column=80)
cerca_quadri_button.grid(row=10, column=80)
stampa_quadri_button.grid(row=11, column=80)
stampa_matricole_html.grid(row=16, column=80)
stampa_quadri_html.grid(row=17, column=80)
stampa_matricole_label.grid(row=15, column=80)
# avvia il loop principale dell'interfaccia grafica

root.geometry("1280x1024")
#elimina_tutti_i_record()




root.mainloop()


    
