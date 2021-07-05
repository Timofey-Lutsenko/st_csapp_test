import sqlite3


conn = sqlite3.connect('csapp.db')

cur = conn.cursor()
conn.execute(""" DROP TABLE IF EXISTS 'tasks' """)
cur.execute(""" CREATE TABLE IF NOT EXISTS 'tasks'
(
task_type VARCHAR(10), 
task_id VARCHAR(100), 
data VARCHAR(255), 
status VARCHAR(25), 
result VARCHAR(255)
)
""")

conn.commit()
