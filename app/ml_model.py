import joblib

model = joblib.load("model/phishing_model.pkl")

def predict_email(text):
    return model.predict([text])[0]
