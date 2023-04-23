import random
import time
import os
import json 
import logging
from paho.mqtt import client as mqtt_client
#from mqtt_database import insert_data


#Authentication to the broker 
BROKER = os.environ.get('BROKER_URL')
BROKER_USERNAME = os.environ.get('BROKER_USERNAME')
BROKER_PASSWORD = os.environ.get('BROKER_PASSWORD')
PORT = 1883

# Topics 
TOPIC_IN = "data/in"
TOPIC_OUT = "data/out"

# All logs store in logs/app.log file 
logging.basicConfig(filename='logs/app.log', level=logging.INFO, 
                    format='%(levelname)s:%(message)s')


# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            logging.info("Connected | RESULT CODE:" + str(rc))
            subscribe(client)
        elif rc == 1:
            print("Connection failed.Incorrect protocol version | RESULT CODE: " + str(rc))
            logging.error("Connection failed. Incorrect protocol version | RESULT CODE: " + str(rc))
        elif rc == 2:
            print("Connection failed. Invalid client identifier | RESULT CODE: " + str(rc))
            logging.error("Connection failed. Invalid client identifier | RESULT CODE: " + str(rc))
        elif rc == 3:
            print("Connection failed. Server error | RESULT CODE: " + str(rc))
            logging.error("Connection failed. Server error | RESULT CODE: " + str(rc))
        elif rc == 4:
            print("Connection failed. Bad username or password | RESULT CODE: " + str(rc))
            logging.error("Connection failed. Bad username or password | RESULT CODE: " + str(rc))
        elif rc == 5:
            print("Connection failed. Not authorised | RESULT CODE: " + str(rc))
            logging.error("Connection failed. Not authorised | RESULT CODE: " + str(rc))
        else:
            print("Connection failed - Unknown | RESULT CODE: Undefined")
            logging.error("Connection failed - Unknown | RESULT CODE: Undefined")

# connect to the broker
def connect_mqtt() -> mqtt_client:
    
    client = mqtt_client.Client(client_id, clean_session=False)
    client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client

def edit_message(msg):
    pass

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")
        logging.error("Unexpected MQTT disconnection. Will auto-reconnect")

#subscribe to the broker
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        json_acceptable_string = msg.payload.decode().replace("'", "\"")
        json_data = json.loads(json_acceptable_string)
        #print(msg)
        print((json_data))
        time.sleep(1)
        
        result = client.publish(TOPIC_OUT, str(msg), qos=1)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{TOPIC_OUT}`")
        else:
            print(f"Failed to send message to topic {TOPIC_OUT}")
            logging.error(f"Connection failed to send message {str(msg)}")
        #insert_data(json_data)
    
    client.on_message = on_message
    client.subscribe(TOPIC_IN)
    
  
def run():
    connected = False
    while not connected: 
        try:
            client = connect_mqtt()
            connected = True
        except:
            print("Waiting for connection to MQTT, retrying in 2 seconds")
            time.sleep(2.0)
    client.on_disconnect = on_disconnect 
    client.loop_forever()


if __name__ == '__main__':
    run()