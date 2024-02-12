import flask
import numpy as np
from flask import Flask, request, url_for, render_template
from flask_bootstrap import Bootstrap
import pickle
import os

#Creating app name
app = Flask(__name__)
Bootstrap(app)

current_dir = os.path.dirname(__file__)
labelencoder_path = os.path.join(current_dir, "models", "labelencoder.pkl")
model_path = os.path.join(current_dir, "models", "model.pkl")

label_encoder = pickle.load(open(labelencoder_path,"rb"))
model = pickle.load(open(model_path,"rb"))

@app.route("/")
def home():
    print("Inside Home")
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    print("Inside Predict method")
    user_inputs = []
    for value in request.form.values():
        if value=='Summer':
            user_inputs.append(1.0)
            break
        elif value=='Winter':
            user_inputs.append(0.0)
            break
        else:
            user_inputs.append(float(value))

    features_array = [np.array(user_inputs)]
    prediction = model.predict(features_array)
    prediction_class = label_encoder.inverse_transform(prediction)

    return render_template("index.html",prediction_text=f"The crop to be cultivated is {prediction_class}")

if __name__ == "__main__":
    app.run(debug=True)


