# Derrived from sample code consumer.py by Aniruddha Gokhale

import os 
import time
from kafka import KafkaConsumer
from pymongo import MongoClient

#connect to kafka
consumer = KafkaConsumer (bootstrap_servers="192.168.5.114:9092", auto_offset_reset='latest') # vm1
consumer.subscribe (topics=["needTopic"])

# connect to mongoDb
uri = "mongodb://192.168.5.110:27017/"
user = "team1"
pw = "team1"
client = MongoClient(uri, connectTimeoutMS=60000, tls=True, username=user, password=pw)
database = client["admin"]
collection = database["iot_data"]

try:

    for msg in consumer:

        print (str(msg.value, 'ascii')) #debugging
        
        #todo: deserialize message
        collection.insert_one({
            "id": msg.value.id,
            "ground_truth": msg.value.GßroundTruth,
            "data": msg.value.Data,
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
