# Derrived from sample code consumer.py by Aniruddha Gokhale

import os 
import time
import requests
from kafka import KafkaConsumer

#connect to kafka
consumer = KafkaConsumer (bootstrap_servers="192.168.5.114:9092", auto_offset_reset='latest') # vm1
consumer.subscribe (topics=["iot_images"])

mlsURL = "192.168.5.110:port" #todo need this port number and possibly end point name

try:

    for msg in consumer:

        print (str(msg.value, 'ascii')) #debugging
        req = requests.post(mlsURL, json = msg.value)
        print(req.text)
        


except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

finally:
    consumer.close()
    
consumer.close()
