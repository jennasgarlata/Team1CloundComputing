# Derrived from sample code consumer.py by Aniruddha Gokhale

import os 
import time
import requests
from kafka import KafkaConsumer
import json

#connect to kafka
consumer = KafkaConsumer (bootstrap_servers="192.168.5.114:9092", auto_offset_reset='latest', value_deserializer=lambda m: json.loads(m.decode('utf-8'))) # vm1
consumer.subscribe (topics=["iot_images"])

mlsURL = "http://192.168.5.110:5000/predict" #todo need this port number and possibly end point name

try:

    for msg in consumer:

        print (msg.value) #debugging
        headers = {'Content-type': 'application/json'}
        req = requests.post(mlsURL, json=msg.value, headers={'Content-type': 'application/json'})
        print(req.text)
        


except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

finally:
    consumer.close()
    
consumer.close()
