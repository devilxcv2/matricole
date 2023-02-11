from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/matricole')
def matricole():
    conn = sqlite3.connect('C:\\Users\\enrico\\Documents\\pythoncode\\mio\\matricole.db')
    c = conn.cursor()
    c.execute("SELECT * FROM matricole")
    data = c.fetchall()
    conn.close()
    return render_template('matricole.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
