from fastapi import FastAPI
from .schemas.review import ReviewReq
from app.ml.predict import predict_review

app = FastAPI(title="imdb-sentiment-analyzer", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/predict")
def predict(request: ReviewReq):
    review = request.review

    prediction, probability = predict_review(review)

    if prediction == 1:
        sentiment = "positive"
        confidence = probability
    else:
        sentiment = "negative"
        confidence = probability

    return {"sentiment": sentiment, "confidence": confidence}
