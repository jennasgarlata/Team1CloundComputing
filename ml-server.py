import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import io
from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json
import base64
from pymongo import MongoClient

# Load a pretrained ResNet model
model = models.resnet18(pretrained=True)
model.eval()
# Define image transformations to match ResNet input requirements
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Flask app for inference
app = Flask(__name__)

# Kafka producer setup
producer_config = {
    'bootstrap.servers': '192.168.5.114:9092'  # Adjust this to your Kafka broker
}
producer = Producer(producer_config)

# connect to mongoDb
uri = "mongodb://192.168.5.110:27017/"
user = "team1"
pw = "team1"
client = MongoClient(uri, connectTimeoutMS=60000, tls=False, directConnection=True, username=user, password=pw)
database = client["admin"]
collection = database["iot_data"]

def send_inference_to_db(record):
    myquery = {"id": record['id']}
    newvalues = { "$set": { "inference": record['inferred_value'] } }
    print(record['id'])
    print(record['inferred_value'])
    collection.update_one(myquery, newvalues)


def process_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = transform(image).unsqueeze(0)  # Add batch dimension
    return image

@app.route('/predict', methods=['POST'])
def predict():
    print(request.json)
    json_data = request.json  # Access the JSON directly
    image_data = json_data.get("Data")
    
    # Decode the base64 image
    image_bytes = base64.b64decode(image_data)

    image_tensor = process_image(image_bytes)

    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted_class = outputs.max(1)

    # Prepare inference result
    result = {
        'id': json_data['ID'],  # DB entry ID
        'inferred_value': predicted_class.item()
    }

    # Send result to Kafka for DB consumer
    send_inference_to_db(result)

    return jsonify({'predicted_class': predicted_class.item()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)