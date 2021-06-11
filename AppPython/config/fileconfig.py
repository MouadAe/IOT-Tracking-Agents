import MySQLdb

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_Topic_Tracking = "testtopic/aouane"
MQTT_Port = 1883
MQTT_Keep_Alive_Interval = 30
dbConnection=""
try :
    dbConnection = MySQLdb.connect(host = "localhost",use= "root",
    passwd= "",db = "people_tracking")
except:
    dbConnection=""
    print("can't connecte !")
host = ""
port = 5555
socketAdd = (host, port)
