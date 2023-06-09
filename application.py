from flask import Flask, request, jsonify, send_from_directory, redirect
#from flask_cors import CORS
#from flask_cors import cross_origin
from keras.models import load_model
from PIL import Image
import tensorflow as tf
import os
import io
import numpy as np

application = app = Flask(__name__, static_folder='build')
#CORS(app)

# Load the h5 model
model = load_model("models/binaryClassifierV2.h5")
classify = load_model("models/multiClass3.h5")

# Define a function to preprocess the image
def preprocess_image(img):
    
    img = tf.image.resize(img, (256, 256))
    
    return img
#@application.route("/")

#def hello_world():
    #return "<p>Hello, World!</p>"
@application.route("/", defaults={"path": ""})
@application.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(application.static_folder + "/" + path):
        return send_from_directory(application.static_folder, path)
    else:
        return send_from_directory(application.static_folder, "index.html")


@application.route("/predict", methods=["POST"])
def predict():
    img = request.files["image"]
    
    if "image" not in request.files:
        return jsonify({"prediction": "No image found"})

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

@application.route("/classify", methods=["POST"])
def classification():
    img = request.files["image"]
    
    if "image" not in request.files:
        return jsonify({"prediction": "No image found"})

    img = img.read()
    img = Image.open(io.BytesIO(img))
    img = preprocess_image(img)
    
    # Make prediction
    result = classify.predict(np.expand_dims(img/255, 0))
    prediction = np.argmax(result)
    if prediction == 0:
        prediction_label = "Anaplasmosis"
    elif prediction == 1:
        prediction_label = "Babesiosis"
    else:
        prediction_label = "Theileriosis"

    response = jsonify({"prediction": prediction_label})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    application.run(debug=True)
