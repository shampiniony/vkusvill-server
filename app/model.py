import os

import joblib


def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "models", "fruit_model.pkl")
    model = joblib.load(model_path)
    return model


model = load_model()


def predict(input_data):
    prediction = model.predict(input_data)
    return prediction
