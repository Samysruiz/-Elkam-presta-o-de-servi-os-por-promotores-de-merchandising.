import sqlite3

conn = sqlite3.connect("duh.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
usuario TEXT,
senha TEXT,
tipo TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS mercados(
id INTEGER PRIMARY KEY AUTOINCREMENT,
mercado TEXT,
endereco TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS produtos(
id INTEGER PRIMARY KEY AUTOINCREMENT,
mercado TEXT,
produto TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS agenda(
id INTEGER PRIMARY KEY AUTOINCREMENT,
funcionario TEXT,
mercado TEXT,
produto TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS relatorio(
data TEXT,
funcionario TEXT,
mercado TEXT,
produto TEXT,
status TEXT,
foto TEXT
)
""")

conn.commit()
