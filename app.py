from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from scraper import scraping

app = Flask(__name__)




def filtra_articoli(keyword=None, fonte=None, data_inizio=None, data_fine=None): # None perchè sono parametri opzionali
    query = "SELECT title, url, source, published_date, summary FROM articles WHERE TRUE" # ho bisogno di una condizione sempre vera per fare la concatenazione
    
    parametri=[] # lista di parametri per la ricerca che vanno al posto dei ? 

    # filtro per parola chiave
    if keyword:
        query += " AND (title LIKE ? OR summary LIKE ?)"
        parametri.extend(["%" + keyword + "%", "%" + keyword + "%"])


    # filtro per fonte
    if fonte:
        query += " AND source = ?"
        parametri.append(fonte)

    # filtro per date
    if data_inizio:
        query += " AND published_date >= date(?) "
        parametri.append(data_inizio)
    if data_fine:
        query += " AND published_date <= date(?) "
        parametri.append(data_fine)

    query += " ORDER BY published_date DESC"

    conn = sqlite3.connect("articoli.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute(query, parametri)
    
    return cur.fetchall()



@app.route("/", methods=["GET"])
def homepage():
    
    keyword = request.args.get("keyword")
    fonte = request.args.get("fonte")
    data_inizio = request.args.get("data_inizio")
    data_fine = request.args.get("data_fine")

    articoli = filtra_articoli(keyword, fonte, data_inizio, data_fine)

    return render_template("homepage.html", articoli=articoli)

    # se l'utente non dovesse inserire alcun filtro, filtra_articoli ritorna comunque cur.fetchall 
    # che contiene la query originale che mostra il contenuto della tabella

@app.route("/scrape", methods=["GET","POST"])
def esecuzione_scraping():
    scraping() # funzione importata da scraper.py
    return render_template("scraping.html")


if __name__ == "__main__":
    app.run(debug=True)