import sqlite3

dbName = "AgentsTracking.db"
TableSchema = """
drop table if exists trakingAgent;
Create Table trakingAgent(
id integer primary key autoincrement,
latitude double,
longitude double,
Date_time text,
type text,
speed double,
id_agent text
);
drop table if exists Agent;
Create Table Agent(
id integer primary key autoincrement,
firstName double,
type text,
isFree INTEGER
)
"""

# Connection
conn = sqlite3.connect(dbName)
curs = conn.cursor()

# Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

curs.close()
conn.close()
