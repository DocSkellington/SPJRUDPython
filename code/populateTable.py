import sqlite3
import os

os.remove("Test.db")
conn = sqlite3.connect("Test.db")
c = conn.cursor()
c.execute("CREATE TABLE Cities (Name VARCHAR(25) NOT NULL, Country VARCHAR(25), Population INTEGER NOT NULL, CONSTRAINT name_pk PRIMARY KEY(Name));")
c.execute("CREATE TABLE Countries (Name VARCHAR(25) NOT NULL, Leader VARCHAR(25), CONSTRAINT leader_pk PRIMARY KEY(Name));")
c.execute("INSERT INTO Cities VALUES('Bruxelles', 'Belgique', 184230)")
c.execute("INSERT INTO Cities VALUES('Paris', 'France', 1234546789)")
c.execute("INSERT INTO Countries VALUES('Belgique', 'C. Michel');")
c.execute("INSERT INTO Countries VALUES('France', 'F. Hollande');")
conn.commit()
conn.close()

