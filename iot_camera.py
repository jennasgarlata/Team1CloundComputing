from kafka import KafkaProducer
import json
import base64
import uuid
from io import BytesIO
from tensorflow.keras.datasets import cifar10
from PIL import Image, ImageFilter
import random


(x_train, y_train), (_, _) = cifar10.load_data()
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


producer = KafkaProducer(
    bootstrap_servers='192.168.5.114:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def add_noise_to_image(image_array):
    """Add noise (blur) to the image."""
    image = Image.fromarray(image_array)
    noise_level = random.uniform(0.5, 2.0)
    noisy_image = image.filter(ImageFilter.GaussianBlur(radius=noise_level))
    return noisy_image

def send_image_to_kafka(image, label):
    """Send the image and its label to the Kafka broker."""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_bytes = base64.b64encode(buffered.getvalue()).decode('utf-8')

    message = {
        'ID': str(uuid.uuid4()),
        'GroundTruth': label,
        'Data': image_bytes
    }

    producer.send('iot_images', message)  
    producer.flush()  

def send_test_message():
    test_message = {
        'message': 'Hello, Kafka!'
    }
    producer.send('iot_images', test_message)  
    producer.flush()  
    print("Test message sent to Kafka!")


for i in range(len(x_train)):
    label = classes[y_train[i][0]]
    noisy_image = add_noise_to_image(x_train[i])
    send_image_to_kafka(noisy_image, label)

send_test_message()


producer.close()
