import sqlite3
import os

DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # यहाँ 'anime' नाम की टेबल बन रही है जिसमें सही कॉलम्स हैं
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()