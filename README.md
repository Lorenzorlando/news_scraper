# News Scraper

News Scraper è un'applicazione che consente di estrarre articoli da varie fonti online, salvarli in un database e consultarli tramite un'interfaccia web con funzionalità di ricerca e filtraggio.

# Funzionalità principali

1. Endpoint per lo scraping
   - URL: '/scrape'
   - Avvia lo scraping degli articoli dalle fonti configurate.
   - Salva automaticamente gli articoli estratti nel database.

2. Pagina principale
   - Mostra la lista completa degli articoli salvati.
   - Ogni articolo include:
     - Titolo
     - Fonte
     - Data di pubblicazione
     - Summary
     - Link alla fonte originale

3. Ricerca e filtri
   - Ricerca per parola chiave presente nel titolo o nel contenuto.
   - Filtri per:
     - Fonte dell'articolo
     - Intervallo di date di pubblicazione

---

## Tecnologie utilizzate
- Python  
- Flask (per il backend e le route)  
- Database SQLite per salvare gli articoli  
- HTML/CSS per la parte frontend
