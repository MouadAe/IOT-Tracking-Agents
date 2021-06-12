# import mysql.connector
import sys
sys.path.append('..')
from  config.fileconfig import *

conn = dbConnection()
# if we can't get the connection so we exit the code
if(conn == False):
    exit()

# cursor = conn.cursor()

# cursor.execute("select * from categorie")

# records = cursor.fetchall()

print("datat ",conn)