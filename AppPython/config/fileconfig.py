import mysql.connector

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_Topic_Tracking = "testtopic/aouane"
MQTT_Port = 1883
MQTT_Keep_Alive_Interval = 30

mysql_db_name ="agentstracking02"

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
            dbConnection()
        except:
            print("data base no exist")
            return False


host = ""
port = 5555
socketAdd = (host, port)
