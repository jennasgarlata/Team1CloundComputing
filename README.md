# Team1CloudComputing

Members: Christy Mugomba, Jonathan Poteet, Jenna Sgarlata

## Deployment Setup

### VM 1: Kafka Broker
Kafka broker running as the message stream manager. It has two components Zookeeper and the Kafka Broker. 

Starts Kafka Broker: 
    
    /kafka/bin/zookeeper-server-start.sh /kafka/config/zookeeper.properties

Starts Zookeeper:

    /kafka/bin/zookeeper-server-start.sh /kafka/config/zookeeper.properties

The Kafka broker accepts connections at 192.168.5.114:9092 when it is ran.
### VM 2: IoT Source
Emulated IoT camera source generating and sending noisy images to Kafka broker.
### VM 3: Database + ML Model Server
MongoDB database for storing IoT data and inference results.

To view the DB using MongoDBCompass, you need to port forward your ssh port. An example of this can be found here:

If you are using the config file:

    ssh -F config.txt -L 27017:localhost:27017 vm3

If you are not using the config file:

    ssh -o ProxyCommand="ssh -i F24_BASTION.pem -W %h:%p cc@129.114.27.250" -i team1Key.pem cc@192.168.5.110 -L 27017:localhost:27017

To check if the MongoDB is running:

    sudo systemctl status mongod

Flask-based ML model server running ResNet to infer on image data set up using Python.

To run the ML server, establish the python source and execute the python file:

    source ml-server-model/bin/activate
    python app.py
### VM 4: Consumers
DB-Consumer: Fetches data from Kafka and stores it in the database set up using Python.
Inference-Consumer: Fetches data from Kafka, sends the image to the ML model server for inference, and updates the database with the result set up using Python.

To run the consumers, establish the python source and execute each consumer in a different terminal:

Prior to running for the first time, run the following commands using pip:

    pip install pymongo
    pip install kafka

For the DB Consumer:

    source consumers/bin/activate
    python consumers/db_consumer.py

For the ML Inference Consumer:

    source consumers/bin/activate
    python consumers/inference_consumer.py

## Other Info/Resources
