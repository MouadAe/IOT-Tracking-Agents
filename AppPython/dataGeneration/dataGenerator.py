import sys,os
sys.path.append(os.getcwd()+'\\AppPython\\dataGeneration')
sys.path.append(os.getcwd()+'\\AppPython\\config')
import threading,json,random
from time import sleep
import paho.mqtt.client as mqtt
import pandas as pd
from datetime import datetime
from agentClasses import *
# from fileconfig import *

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
curs = db.cursor()

DATE_LIST = pd.date_range(end=datetime.today(),periods=10).to_pydatetime().tolist()

Keep_Alive_Interval = 30
agents_lenght=50

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

    for i in range(1,agents_lenght) :
        print("--------------------------RANDOM-------------------------------------")
        trakingData = TrakingAgent(
            round(random.uniform(latitude - 0.03,latitude + 0.03), 6),  # latitude
            round(random.uniform(longitude - 0.03,longitude + 0.03), 6),  # longitude
            str(random.choice(DATE_LIST)),  # date_time
            i # id_agent
        )
        gpsJsonData = json.dumps(trakingData.__dict__)
        print(gpsJsonData)

        print("---------------------------------------------------------------------")
        publishToTopic(MQTT_Topic_Tracking, gpsJsonData)
        # sleep(1)


def generate_agentData():
    if(tableIsEmpty() == True):
        for i in range(1,agents_lenght):
            random_agent_type = random.choice([ENUM_AgentType.client.value,ENUM_AgentType.taxi.value])
            random_hold_state = random.choice([True,False])
            agentData = Agent("A_"+str(i),random_agent_type,random_hold_state)
            print(agentData.__dict__)
            try:
                    sql = """insert into Agent(firstName,type,isFree) values(%s,%s ,%s )"""
                    curs.execute(sql, [agentData.firstName,agentData.type,agentData.isFree])
                    db.commit()
            except:
                print("error instert into agent db")
    else:
        print("DB isn't empty")



def tableIsEmpty():
    try:
        sql="""select count(*) from Agent"""
        curs.execute(sql)
        (number_of_rows,)=curs.fetchone()
        if number_of_rows != 0 :
            return False
        else:
            return True
    except:
        print("error in db")




generate_agentData()


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_BROKER, int(MQTT_Port),int(MQTT_Keep_Alive_Interval))

# publishDataToMqtt()

# .A           p1=37.4 p2=38 p3 p4 