# imdb-sentiment-analyzer

Binary sentiment classification on IMDb movie reviews, served over a FastAPI
HTTP API. Training and experiment tracking are done in notebooks with MLflow.

## Stack

| Layer     | Choice                             |
| --------- | ---------------------------------- |
| API       | FastAPI + Uvicorn                  |
| ML        | scikit-learn, NLTK, datasets       |
| Tracking  | MLflow (SQLite backend)            |
| Packaging | uv                                 |
| Runtime   | Docker + Docker Compose            |

## Model

The trained pipeline is a TF-IDF + linear SVM classifier, serialized with
joblib to `models/sentiment_pipeline.pkl`:

```
Pipeline([
  ('tfidf',      TfidfVectorizer(max_features=50000, ngram_range=(1, 2))),
  ('classifier', LinearSVC()),
])
```

Input is expected to be lowercased with `<br />` HTML line breaks stripped and
whitespace collapsed, matching `app/ml/preprocess.py`.

## API

Two endpoints, both defined in `app/main.py`:

| Method | Path       | Description                                   |
| ------ | ---------- | --------------------------------------------- |
| `GET`  | `/`        | Health check, returns `{"message": "hello world"}` |
| `POST`  | `/predict` | Classify a review, body `{"review": "<text>"}`  |

Response shape:

```json
{ "sentiment": "positive", "confidence": 0.923756209214436 }
```

`sentiment` is `"positive"` or `"negative"`. `confidence` is the raw
`LinearSVC.decision_function` margin, so it is signed: positive values indicate
positive sentiment, negative values indicate negative sentiment. It is not a
calibrated probability. A malformed body returns `422`.

Example:

```bash
curl -X POST localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"review":"A masterpiece, I loved every minute of it."}'
```

Note that `/predict` is currently registered as a `GET` with a request body.
That is unusual for an endpoint that takes input; `POST` would be the more
conventional choice if you want to change it.

## Project layout

```
imdb-sentiment-analyzer/
├── app/
│   ├── main.py               # FastAPI app and both endpoints
│   ├── ml/
│   │   ├── preprocess.py     # clean_text: lowercase, strip <br/>, collapse whitespace
│   │   └── predict.py        # predict_review: loads pipeline, returns (label, margin)
│   └── schemas/
│       └── review.py         # ReviewReq pydantic model
├── models/
│   └── sentiment_pipeline.pkl
├── notebooks/
│   ├── 01_exploration.ipynb  # load IMDb dataset, EDA
│   ├── 02_processing.ipynb   # text cleaning layer
│   ├── 03_train_modlel.ipynb # training, hyperparameter experiments, metrics
│   └── 04_mlfloe.ipynb       # log model to MLflow, test prediction
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Setup

Requires Python 3.14 (see `.python-version`).

```bash
uv sync
```

## Run locally

```bash
uv run uvicorn app.main:app --reload
```

Interactive API docs at http://localhost:8000/docs

## Run with Docker

```bash
docker compose up --build
```

| Service  | URL                    | Description        |
| -------- | ---------------------- | ------------------ |
| `api`    | http://localhost:8000 | FastAPI service    |
| `mlflow` | http://localhost:5000 | MLflow tracking UI |

MLflow runs against a SQLite backend stored in the `mlflow-data` volume. To
point local notebook runs at the container instance:

```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
```

## Retraining

The pipeline lives in the notebooks, not in a script. To retrain, run them in
order and write the result to `models/sentiment_pipeline.pkl`:

1. `notebooks/01_exploration.ipynb` loads `stanfordnlp/imdb` and inspects it.
2. `notebooks/02_processing.ipynb` applies the cleaning from
   `app/ml/preprocess.py`.
3. `notebooks/03_train_modlel.ipynb` compares vectorizer/classifier
   combinations and reports accuracy, precision, recall, and F1.
4. `notebooks/04_mlfloe.ipynb` registers the chosen model to MLflow and
   exercises inference.

Notebook output is not version controlled. `mlruns/` and the SQLite tracking
files are gitignored, since runs are reproducible from the notebooks.

## Lint

```bash
uv run ruff check .
```

`ruff` also checks notebook cells, which currently report import-order and
unused-import warnings. Scope it to `app/` to check only the served code.

## Generated files

These are produced at runtime and are gitignored:

- `models/*.pkl` — trained pipeline. Required for `/predict` to work; if it is
  missing, the endpoint fails with `FileNotFoundError`.
- `mlflow.db`, `mlruns/` — MLflow tracking store and artifacts.
