import paho.mqtt.client as mqtt
import sqlite3
import json
import mysql.connector
import MySQLdb
import sys,os
sys.path.append(os.getcwd()+'\\AppPython\\dataGenerationcle')
sys.path.append(os.getcwd()+'\\AppPython\\config')
# from fileconfig import *

'''
dbName = "PeopleTracking.db"
conn = sqlite3.connect(dbName)
curs = conn.cursor()
'''
#---------------------------------------------------start config-----------
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
#----------------------------------------end config-------------------------------

db = dbConnection()
if(db==False):
    exit()

curs = db.cursor()


def insertData(data):
    jsonData = json.loads(data)
    latitude = jsonData["latitude"]
    longitude = jsonData["longitude"]
    Date_time = jsonData["date_time"]
    speed = float(1)
    id_agent = jsonData["id_agent"]
    try:
        sql = """insert into gps_tracking(latitude,longitude,date_time,speed,id_agent) values(%s,%s ,%s ,%s,%s)"""
        curs.execute(sql, [latitude, longitude, Date_time, speed,id_agent])
        db.commit()
        print("------- Data Inserted ---------")
    except MySQLdb.Error as e:
        print(e)
# insertData(json.dumps({"Sensor_ID": "GPS 192.168.1.106", "Date": "13-Jun-2021 01:36:34:885205", "lat": "33.573806", "lon": "-7.555822", "alt": "120.6"}))

def on_connect(self,mosq, obj, rc):
    if rc == 0:
        print("Connected")
        mqttc.subscribe(MQTT_Topic_Tracking, 0)  # Subscribe to all sensors at Base Topic
    else:
        print("Bad Connection")


def on_message(mosq, obj, msg):
    # this is the Master call for saving MQTT Date into DB
    print("MQTT Data Received ...")
    print("MQTT Topic: " + msg.topic)
    jsonData = str(msg.payload).split("'")[1]
    print("Data: " + jsonData)
    insertData(jsonData)
    # print(str(msg.payload).split("'")[1])


def on_subscribe(mosq, obj, mid, granted_qos):
    pass


# MQTT Settings
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect & Subscribe
mqttc.connect(MQTT_BROKER, int(MQTT_Port), int(MQTT_Keep_Alive_Interval))
mqttc.subscribe((MQTT_Topic_Tracking, 0))

mqttc.loop_forever()  # Continue the network loop

# broker = 'mqtt.localdomain'
# broker_port = 1883
# broker_topic = '/test/location/#'
# #broker_clientid = 'mqttuide2mysqlScript'
# #mysql config
# mysql_server = 'thebeast.localdomain'
# mysql_username = 'root'
# mysql_passwd = ''
# mysql_db = 'mqtt'
#change table below.
