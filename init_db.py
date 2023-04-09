import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO trips (record, starred, deptdate, arrivdate, carrier, flight, deptair, arrivair) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ('RecordA',0, "2022-01-01", "2022-01-01", "DL", "317", "JFK", "SEA")
            )

cur.execute("INSERT INTO trips (record, starred, deptdate, arrivdate, carrier, flight, deptair, arrivair) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ('RecordB',1, "2023-04-25", "2023-04-25", "DL", "317", "JFK", "SEA")
            )

connection.commit()
connection.close()
