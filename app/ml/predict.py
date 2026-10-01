import joblib


def predict_review(review: str) -> str:
    model = joblib.load("models/sentiment_pipeline.pkl")

    prediction = model.predict([review])[0]
    probabilities = model.decision_function([review])[0]

    return prediction, probabilities
