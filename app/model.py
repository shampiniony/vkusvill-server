import os

import joblib


def load_model():
    model = joblib.load("./models/fruit_model.pkl")
    return model


model = load_model()


def predict(input_data):
    prediction = model.predict([input_data])
    return prediction[0]
