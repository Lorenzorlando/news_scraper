import sqlite3

conn = sqlite3.connect("articoli.db") # mi connetto e creo il db articoli
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, title TEXT UNIQUE, url TEXT, source TEXT, published_date DATE, summary TEXT, scraped_at DATETIME)")