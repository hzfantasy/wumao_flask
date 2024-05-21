import sqlite3

conn = sqlite3.connect('database.db')

with open('db.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", 
            ('learn Flask1', 'follow Wumao PartI')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", 
            ('learn Flask2', 'follow Wumao PartII')
            )

conn.commit()
conn.close()
