import flask
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

#Creating app name
app = Flask("Crop_Recommender")

model = pickle.load(open("DUMMY.pkl","rb"))
 
@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    features = [float(x) for x in request.form.values()]
    features_array = [np.array(features)]
    prediction = model.predict(features_array)

    return render_template("index.html",prediction_text=f"The crop to be cultivated is {prediction}")

if __name__ == "__main__":
    app.run(debug=True)