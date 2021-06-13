import sys,os
sys.path.append(os.getcwd()+'\\AppPython\\dataGeneration')
sys.path.append(os.getcwd()+'\\AppPython\\config')
import random
import threading
import json
from datetime import datetime
from time import sleep
import re
import paho.mqtt.client as mqtt
from pynput import keyboard
import socket
import traceback
import time
# from fileconfig import MQTT, socketAdd 
from dataGenerator import publishDataToMqtt
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


def on_press(key):
    global break_program
    print(key)
    if key == keyboard.Key.space:
        print('end pressed')
        break_program = True
    return False


def map_msg_to_json(lst, addr):
    dic = {}
    dic['id_agent'] = 'GPS ' + str(addr)
    dic['date_time'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
    dic['latitude'] = lst[3].strip()
    dic['longitude'] = lst[4].strip()
    # dic['alt'] = lst[5].strip()
    return json.dumps(dic)


def on_connect(client, userdata, rc):
    if rc != 0:
        pass
        print("Unable to connect to MQTT Broker...")
    else:
        print("Connected with MQTT Broker: " + str(MQTT_BROKER))


def on_publish(client, userdata, mid):
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass


def publish_to_topic(topic, message):
    mqttc.publish(topic, message)
    print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
    print("")


# MQTT Settings

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_BROKER, int(MQTT_Port), int(MQTT_Keep_Alive_Interval))

break_program = False

# socket.gethostbyname(socket.gethostname())------------------------------------------------------------------------------------------

# SOCK_DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(socketAdd)

# s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# syntax = {
#     1:  ['gps', 'lat', 'lon', 'alt'],     # deg, deg, meters MSL WGS84
#     3:  ['accel', 'x', 'y', 'z'],         # m/s/s
#     4:  ['gyro', 'x', 'y', 'z'],          # rad/s
#     5:  ['mag', 'x', 'y', 'z'],           # microTesla
#     6:  ['gpscart', 'x', 'y', 'z'],       # (Cartesian XYZ) meters
#     7:  ['gpsv', 'x', 'y', 'z'],          # m/s
#     8:  ['gpstime', ''],                  # ms
#     81: ['orientation', 'x', 'y', 'z'],   # degrees
#     82: ['lin_acc',     'x', 'y', 'z'],
#     83: ['gravity',     'x', 'y', 'z'],   # m/s/s
#     84: ['rotation',    'x', 'y', 'z'],   # radians
#     85: ['pressure',    ''],              # ???
#     86: ['battemp', ''],                  # centigrade

#     # Not exactly sensors, but still useful data channels:
#     -10: ['systime', ''],
#     -11: ['from', 'IP', 'port'],
# }
dataIsGenerated = False

dic = {}
with keyboard.Listener(on_press=on_press) as listener:
    print(f"[LISTENING] Server is listening on {s}")
    while break_program == False:
        try:
            # message, address = s.recvfrom(8192)
            message, (peerIP, peerport) = s.recvfrom(8192)

            lst = re.split("[,\'']", str(message))

            if int(lst[2]) == 1:
                message_Json_Data:dict = map_msg_to_json(lst, peerIP)
                publish_to_topic(MQTT_Topic_Tracking, message_Json_Data)

                print("====>",peerIP, '  ', message_Json_Data)
                if(dataIsGenerated == False):
                    publishDataToMqtt(float(lst[3].strip()),float(lst[4].strip()))
                    dataIsGenerated = True
                
                # if address not in dic:
                #     dic[address]=list()
                #     dic[address].append(acceleration_Json_Data)
                # else:
                #     dic[address].append(acceleration_Json_Data)

                # print(message)
                sleep(5)  # make a pause
        except:
            print("exeption ", break_program)
            traceback.print_exc()

    listener.join()
