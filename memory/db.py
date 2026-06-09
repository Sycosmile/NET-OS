import sqlite3

def init_db():
    conn = sqlite3.connect("netos.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, event TEXT)")
    conn.commit()
    conn.close()
