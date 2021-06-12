import mysql.connector
from fileconfig import dbConnection

def creatTables():
    print("-------------------")
    TableSchema = '''
    Create Table Agent(
    id integer primary key AUTO_INCREMENT,
    firstName double,
    type text,
    isFree INTEGER
    )
    '''
    sql ='''Create Table gps_tracking(
    id integer primary key AUTO_INCREMENT,
    latitude double,
    longitude double,
    Date_time text,
    speed double,
    id_agent text
    )'''
    # Connection
    conn = dbConnection()
    curs = conn.cursor()
    curs.execute("DROP TABLE IF EXISTS gps_tracking")
    curs.execute("DROP TABLE IF EXISTS agent")
    # Tables
    curs.execute(sql)
    curs.execute(TableSchema)
    
    print("tables created")

creatTables()

# curs.close()
# conn.close()


