import agentClasses as ac
# obj = ac.Agent("mouad",ac.ENUM_AgentType.client.value,True)
# print(obj.type)
import threading
import paho.mqtt.client as mqtt
import json
import random
import pandas as pd
from datetime import datetime

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_Topic = "testtopic/aouane"

DATE_LIST = pd.date_range(end = datetime.today(), periods=10).to_pydatetime().tolist()

MQTT_Port = 1883
Keep_Alive_Interval = 30
def on_connect(client,userdata,rc):
    if rc !=0:
        pass
        print("Unable to connect to broker")
    else :
        print("Connected with MQTT Broker :"+str(MQTT_BROKER))

def on_publish(client,userdata,mid):
    pass

def on_disconnect(client,userdata,rc):
    if rc!=0:
        pass

def publishToTopic(topic,message):
    mqttc.publish(topic,message)
    print("Publish message : "+str(message)+ " to topic : "+str(topic))
    print("")


def publishDataToMqtt():
    threading.Timer(2.0,publishDataToMqtt).start()
    agentData = ac.TrakingAgent(
      round(random.uniform(33.580000, 33.588888), 6) ,#latitude
      round(random.uniform(-7.600000, -7.610000), 6) ,#longitude
      str(random.choice(DATE_LIST)), #date_time
      random.randint(1, 70) #id_agent
    )
   #  gpsData = {}
   #  gpsData['latitude'] = round(random.uniform(33.580000, 33.588888), 6)
   #  gpsData['longitude'] = round(random.uniform(-7.600000, -7.610000), 6)
   #  gpsData['time'] = str(random.choice(DATE_LIST))
   #  gpsData['speed'] = float((random.randint(1, 5)))
   #  gpsData['id'] = random.randint(1, 500)
    gpsJsonData = json.dumps(agentData.__dict__)

    publishToTopic(MQTT_Topic,gpsJsonData)

mqttc=mqtt.Client()
mqttc.on_connect=on_connect
mqttc.on_disconnect=on_disconnect
mqttc.on_publish=on_publish
mqttc.connect(MQTT_BROKER,int(MQTT_Port),int(Keep_Alive_Interval))

publishDataToMqtt()