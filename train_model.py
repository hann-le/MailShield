
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

df = pd.read_csv("data/emails.csv")
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(df["text"], df["label"])
joblib.dump(model, "model/phishing_model.pkl")