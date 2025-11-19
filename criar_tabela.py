import sqlite3

con = sqlite3.connect("agenda.db")
con.execute("""
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data TEXT NOT NULL
)
""")
con.commit()
con.close()

print("Tabela criada!")

