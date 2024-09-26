# Import necessary libraries
from kafka import KafkaProducer 
import json 
import base64 
import uuid  
from io import BytesIO  
from tensorflow.keras.datasets import cifar10 
from PIL import Image, ImageFilter 
import random  
import time 

# Load the CIFAR-10 dataset
(x_train, y_train), (_, _) = cifar10.load_data()  
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Create a Kafka producer instance
producer = KafkaProducer(
    bootstrap_servers='192.168.5.114:9092', 
    value_serializer=lambda v: json.dumps(v).encode('utf-8') 
)

# Function to add Gaussian noise to an image
def add_noise_to_image(image_array):
    image = Image.fromarray(image_array)  
    noise_level = random.uniform(0.5, 2.0)  
    noisy_image = image.filter(ImageFilter.GaussianBlur(radius=noise_level))
    return noisy_image 

# Function to send an image and its label to Kafka
def send_image_to_kafka(image, label):
    buffered = BytesIO()  
    image.save(buffered, format="JPEG")  
    image_bytes = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Create a message dictionary with a unique ID, label, and image data
    message = {
        'ID': str(uuid.uuid4()),  
        'GroundTruth': label,  
        'Data': image_bytes 
    }

    # Send the message to the 'iot_images' topic
    producer.send('iot_images', message)
    producer.flush() 

# Function to send a test message to Kafka
def send_test_message():
    test_message = {
        'message': 'Hello, Kafka!' 
    }
    producer.send('iot_images', test_message) 
    producer.flush() 
    print("Test message sent to Kafka!")  

# Specify the number of images to send
num_images_to_send = 10

# Loop through the training images and send them to Kafka
for i in range(min(len(x_train), num_images_to_send)):  
    label = classes[y_train[i][0]]  
    noisy_image = add_noise_to_image(x_train[i])  
    send_image_to_kafka(noisy_image, label) 
    print(f"Image {i + 1} sent to Kafka with label '{label}'") 
    time.sleep(1)  # Wait for 1 second before sending the next image

# Uncomment the following line to for a test message (optional)
# send_test_message()

# Close the Kafka producer
producer.close()
