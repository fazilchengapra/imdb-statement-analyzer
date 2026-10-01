from fastapi import FastAPI

from app.ml.predict import predict_review

from .schemas.review import ReviewReq

app = FastAPI(title="imdb-sentiment-analyzer", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post("/predict")
def predict(request: ReviewReq):
    review = request.review

    prediction, probability = predict_review(review)

    if prediction == 1:
        sentiment = "positive"
        confidence = probability
    else:
        sentiment = "negative"
        confidence = probability

    return {"sentiment": sentiment, "row_score": confidence}
