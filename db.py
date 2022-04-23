import os
import pickle
import sqlite3
import pandas as pd

data = pd.read_csv('data2.csv')

conn = sqlite3.connect('project.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Project;")
cur.execute("""CREATE TABLE Project(id INTEGER PRIMARY KEY NOT NULL,
summoners VARCHAR(128),
result INTEGER,
time INTEGER,
champion VARCHAR(128),
d_spell VARCHAR(128),
f_spell VARCHAR(128),
kill INTEGER,
deaths INTEGER,
assist INTEGER,
level INTEGER,
kill_part INTEGER,
cs INTERGER,
ward INTEGER,
kda FLOAT)""")

for i in range(len(data)):
    lst = [i]
    lst.append(data['summoners'][i])
    lst.append(str(data['result'][i]))
    lst.append(str(data['time'][i]))
    lst.append(data['champion'][i])
    lst.append(data['d_spell'][i])
    lst.append(data['f_spell'][i])
    lst.append(str(data['kill'][i]))
    lst.append(str(data['deths'][i]))
    lst.append(str(data['assist'][i]))
    lst.append(str(data['level'][i]))
    lst.append(str(data['kill_part'][i]))
    lst.append(str(data['cs'][i]))
    lst.append(str(data['ward'][i]))
    lst.append(data['kda'][i])
    cur.execute("INSERT INTO Project VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", lst)

conn.commit()
cur.close()
conn.close()