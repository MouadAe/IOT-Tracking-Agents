import mysql.connector
from time import sleep

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_Topic_Tracking = "iot/smartTaxi/tracking"
MQTT_Port = 1883
MQTT_Keep_Alive_Interval = 30

mysql_db_name ="agentstracking"

def dbConnection():
    try :
        conn =mysql.connector.connect(host = "localhost",port="3306",user= "root",
        passwd= "",db = mysql_db_name)
        return conn
    except:
        try : 
            conn =mysql.connector.connect(host = "localhost",port="3306",user= "root",
            passwd= "")
            mycursor = conn.cursor()
            mycursor.execute("CREATE DATABASE "+mysql_db_name) 
            sleep(2) 
            dbConnection()
        except:
            print("error db")
            return False



host = ""
port = 5555
socketAdd = (host, port)
