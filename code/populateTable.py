import sqlite3
import os

os.remove("Test.db")
conn = sqlite3.connect("Test.db")
c = conn.cursor()
c.execute("CREATE TABLE Cities (Name VARCHAR(25) NOT NULL, Country VARCHAR(25), Population INTEGER NOT NULL, CONSTRAINT name_pk PRIMARY KEY(name));")
c.execute("INSERT INTO Cities VALUES('Paris', 'France', 2564)")
conn.commit()
conn.close()

