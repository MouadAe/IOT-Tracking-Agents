import paho.mqtt.client as mqtt
import sqlite3
import json
import mysql.connector
import MySQLdb
import sys
sys.path.append('..')
from  config.fileconfig import *
'''
dbName = "PeopleTracking.db"
conn = sqlite3.connect(dbName)
curs = conn.cursor()
'''

db = dbConnection
curs = db.cursor()



def insertData(data):
    jsonData = json.loads(data)
    latitude = jsonData["latitude"]
    longitude = jsonData["longitude"]
    Date_time = jsonData["time"]
    speed = float(jsonData["speed"])
    citizen_id = int(jsonData["id"])
    try:

        sql = """insert into gps_log(latitude,longitude,date_time,speed,citizen_id) values(%s,%s ,%s ,%s,%s)"""
        curs.execute(sql, [latitude, longitude, Date_time, speed,citizen_id])
        db.commit()
        print("------- Data Inserted ---------")
    except MySQLdb.Error as e:
        print(e)


def on_connect(mosq, obj, rc):
    if rc == 0:
        print("Connected")
        mqttc.subscribe(MQTT_Topic_Tracking, 0)  # Subscribe to all sensors at Base Topic
    else:
        print("Bad Connection")


def on_message(mosq, obj, msg):
    # this is the Master call for saving MQTT Date into DB
    print("MQTT Data Received ...")
    print("MQTT Topic: " + msg.topic)
    # print("MQTT Message: " + str(msg.payload))
    jsonData = str(msg.payload).split("'")[1]
    print("Data: " + jsonData)
    insertData(jsonData)


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

broker = 'mqtt.localdomain'
broker_port = 1883
broker_topic = '/test/location/#'
#broker_clientid = 'mqttuide2mysqlScript'
#mysql config
mysql_server = 'thebeast.localdomain'
mysql_username = 'root'
mysql_passwd = ''
mysql_db = 'mqtt'
#change table below.
