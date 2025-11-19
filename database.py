import sqlite3
con = sqlite3.connect("agenda.db") ##Caderno
cursor = con.cursor() ##Caneta
cursor.execute(""" CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL) """)

con.commit()
con.close()



