# Derrived from sample code consumer.py by Aniruddha Gokhale

import os 
import time
from kafka import KafkaConsumer
from pymongo import MongoClient
import json

#connect to kafka
consumer = KafkaConsumer (bootstrap_servers="192.168.5.114:9092", auto_offset_reset='latest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))  # Deserialize the message from bytes to JSON) # vm1
consumer.subscribe (topics=["iot_images"])

# connect to mongoDb
uri = "mongodb://192.168.5.110:27017/"
user = "team1"
pw = "team1"
client = MongoClient(uri, connectTimeoutMS=60000, tls=False, directConnection=True, username=user, password=pw)
database = client["admin"]
collection = database["iot_data"]

try:

    for msg in consumer:

        print(msg.value)  # debugging
        
        #todo: deserialize message
        collection.insert_one({
            "id": msg.value.get("ID"),
            "ground_truth": msg.value.get("GroundTruth"),
            "data": msg.value.get("Data"),
            "inference": ""
        })

        # without inf field:     collection.insert_one(message)ß

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

finally:
    client.close()
    consumer.close()
    
client.close()
consumer.close()
