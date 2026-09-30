from fastapi import FastAPI

app = FastAPI(
    title='imdb-sentiment-analyzer',
    version='1.0.0'
)

@app.get('/')
async def root():
    return {'message':'hello world'}