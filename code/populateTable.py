import sqlite3

conn = sqlite3.connect("Test.db")
c = conn.cursor()
c.execute("CREATE TABLE Cities (name VARCHAR(25), Country VARCHAR(25), CONSTRAINT name_pk PRIMARY KEY(name));")
c.execute("INSERT INTO Cities VALUES('Paris', 'France')")
conn.commit()
conn.close()

