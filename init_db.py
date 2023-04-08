import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO trips (record, starred) VALUES (?, ?)",
            ('RecordA',0)
            )

cur.execute("INSERT INTO trips (record, starred) VALUES (?, ?)",
            ('RecordB',1)
            )

connection.commit()
connection.close()
