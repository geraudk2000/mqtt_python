import random
import time
from paho.mqtt import client as mqtt_client
import os

BROKER = os.environ.get('BROKER_URL')
PORT = 1883
TOPIC = "data/in"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000000)}'
broker_username = os.environ.get('BROKER_USERNAME')
broker_password = os.environ.get('BROKER_PASSWORD')

#generate a random payload to send to the broker
def message_gen(): 
    message = {
        "ID" : random.randint(0, 1000000),
        "NAME": "temperature",
        "TYPE": "float",
        "MIN_VALUE": 30,
        "MAX_VALUE": 40,
        "MAX_STEP": 0.2
    }
    return message

#connect to the broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id, clean_session=False)
    client.username_pw_set(broker_username, broker_password)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


# Publish message to the broker
def publish(client):

    while True:
        data =  message_gen()
        time.sleep(1)
        msg = str(data)
        #msg = f"messages: {data}"
        #print(type(msg))
        result = client.publish(TOPIC, msg, qos=1, retain=False)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{TOPIC}`")
        else:
            print(f"Failed to send message to topic {TOPIC}")
        

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()