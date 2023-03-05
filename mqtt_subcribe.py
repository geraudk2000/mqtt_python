import random
import os
import json 
from paho.mqtt import client as mqtt_client
from mqtt_database import insert_data


broker = os.environ.get('BROKER_URL')
#Authentication to the broker 
broker_username = os.environ.get('BROKER_USERNAME')
broker_password = os.environ.get('BROKER_PASSWORD')
port = 1883
topic = "python/mqtt"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

# connect to the broker
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(broker_username, broker_password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


#subscribe to the broker
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        json_acceptable_string = msg.payload.decode().replace("'", "\"")
        json_data = json.loads(json_acceptable_string)
        print(json_data)
        #print(type(json_data))
        insert_data(json_data)
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()