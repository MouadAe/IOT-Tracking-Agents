from .agentClasses import Agent, TrakingAgent
import threading
import paho.mqtt.client as mqtt
import json
import random
import pandas as pd
from datetime import datetime
from ..config.fileconfig import MQTT_BROKER, MQTT_Keep_Alive_Interval, MQTT_Port, MQTT_Topic_Tracking


DATE_LIST = pd.date_range(end=datetime.today(),
                          periods=10).to_pydatetime().tolist()

Keep_Alive_Interval = 30


def on_connect(client, userdata, rc):
    if rc != 0:
        pass
        print("Unable to connect to broker")
    else:
        print("Connected with MQTT Broker :"+str(MQTT_BROKER))


def on_publish(client, userdata, mid):
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass


def publishToTopic(topic, message):
    mqttc.publish(topic, message)
    print("Publish message : "+str(message) + " to topic : "+str(topic))
    print("")


def publishDataToMqtt(latitude, longitude):
    threading.Timer(2.0, publishDataToMqtt).start()
    agentData = TrakingAgent(
        round(random.uniform(latitude-0.008888,
              latitude + 0.008888), 6),  # latitude
        round(random.uniform(longitude - 0.05,
              longitude + 0.05), 6),  # longitude
        str(random.choice(DATE_LIST)),  # date_time
        random.randint(1, 70)  # id_agent
    )
    gpsJsonData = json.dumps(agentData.__dict__)

    publishToTopic(MQTT_Topic_Tracking, gpsJsonData)


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_BROKER, int(MQTT_Port),
              int(MQTT_Keep_Alive_Interval))

# publishDataToMqtt()
