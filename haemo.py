from flask import Flask, request, jsonify
import base64
from flask_cors import CORS
from flask_cors import cross_origin
from keras.models import load_model
from PIL import Image
import base64
import tensorflow as tf
from PIL import Image
import io

#from keras.preprocessing import image
import keras.utils as image
import numpy as np
import json
from werkzeug.datastructures import ImmutableMultiDict


app = Flask(__name__)
CORS(app)

# Load the h5 model
model = load_model("imageclassifier.h5")

# Define a function to preprocess the image
def preprocess_image(img):
    #img = image.load_img(img, target_size=(256, 256))
    img = tf.image.resize(img, (256, 256))
    #img = image.img_to_array(img)
    #img = np.expand_dims(img, axis=0)
    #img = img / 255.0  # Normalize pixel values
    return img

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/predict", methods=["POST"])

def predict():
    # Check if image is uploaded
    
    img = request.files["image"]
    
    if "image" not in request.files:
        return jsonify({"prediction": "No image found"})

    # Get the uploaded image
    #img = request.form
    #if request.method == "POST":
        #img = request.files["image"]
    #img = request.files["image"]
    #print(img)
    # Preprocess the image
    #img = base64.b64encode(img.read()).decode('utf-8')
    img = img.read()
    img = Image.open(io.BytesIO(img))
    img = preprocess_image(img)
    

    # Make prediction
    prediction = model.predict(np.expand_dims(img/255, 0))
    # Get the predicted class label (assuming binary classification)
    prediction_label = "Blood sample has haemoprotozoan infection" if prediction > 0.5 else "Blood sample is not infected"

    response = jsonify({"prediction": prediction_label})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(debug=True)
