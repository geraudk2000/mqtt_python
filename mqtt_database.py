import pymongo
import os

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

def insert_data(msg):
    client = pymongo.MongoClient("mongodb+srv://"+ db_user + ":" + db_password + "@mqtt.cyklxjs.mongodb.net/?retryWrites=true&w=majority")
    db = client.db_mqtt
    collection = db['collection_mqtt']
    collection.insert_one(msg).inserted_id
    client.close()
