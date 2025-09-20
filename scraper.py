import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from email.utils import parsedate_to_datetime
import html


RSS_giornali = {
    "ANSA": "https://www.ansa.it/sito/notizie/topnews/topnews_rss.xml",
    "Corriere della sera": "https://www.corriere.it/rss/homepage.xml",
    "Repubblica": "https://www.repubblica.it/rss/homepage/rss2.0.xml",
    "Ilsole24ore": "https://www.ilsole24ore.com/rss/italia.xml"
}

# Connessione al DB 
conn = sqlite3.connect("articoli.db", check_same_thread=False) # per poter utilizzare l'oggetto anche in altri file
cur = conn.cursor()


def inserimento_articolo(title, url, source, published_date, summary):
    try:
        dt = parsedate_to_datetime(published_date) # legge le date recuperate dallo scraper che sono nel formato Wed, 10 Sep 2025...
        published_date = dt.strftime("%Y-%m-%d") # converto la data nel formato YY-MM-DD così da non avere problemi poi nelle operazioni con le date 
        
        cur.execute("""
            INSERT INTO articles (title, url, source, published_date, summary, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, url, source, published_date, summary, datetime.today() ))
        conn.commit() # conferma l'inserimento nel db
    except sqlite3.IntegrityError: # se c'è un vincolo di unicità non inserisce l'articolo con URL che è già presente
        print("Errore")
      

def scraping():
    for fonte, url in RSS_giornali.items(): # scorro items che contiene la coppia chiave valore (fonte e url)
        resp = requests.get(url) # invia una richiesta HTTP GET all URL del feed RSS
        resp.raise_for_status() # se la richiesta non va a buon fine solleva eccezione
        
        soup = BeautifulSoup(resp.content, "xml") # oggetto da cui posso estrarre titolo, link ecc. 
        # .content non fa alcuna decodifica 

        for articolo in soup.find_all("item"):  # scorro i tag "item", ovvero gli articoli
            titolo =  html.unescape(articolo.title.text) if articolo.title else "" # cerco il tag titolo nell'articolo e assegno il relativo testo. Se non lo trova stringa vuota
            link = articolo.link.text if articolo.link else ""
            pub_date = articolo.pubDate.text if articolo.pubDate else ""
            summary = articolo.description.text if articolo.description else ""
            inserimento_articolo(titolo, link, fonte, pub_date, summary)
            # html.unescape serve per evitare problemi con caratteri accentati