import sqlite3

connection = sqlite3.connect("steam_db.sqlite")

connection.execute("""
    CREATE TABLE steam (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        quantity INTEGER
    )
""")
