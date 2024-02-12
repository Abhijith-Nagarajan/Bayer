import flask
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

#Creating app name
app = Flask("Crop_Recommender")

label_encoder = pickle.load(open("E:\Bayer\Crop_Recommendation\labelencoder.pkl","rb"))
model = pickle.load(open("E:\Bayer\Crop_Recommendation\model.pkl","rb"))

 
@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    features = []
    for feature in  request.form.values():
        print(feature)
    #features = [float(x) for x in request.form.values()]
    features_array = [np.array(features)]
    prediction = model.predict(features_array)
    prediction_class = label_encoder.inverse_transform(prediction)

    return render_template("index.html",prediction_text=f"The crop to be cultivated is {prediction_class}")

if __name__ == "__main__":
    app.run(debug=True)