# imdb-sentiment-analyzer

Sentiment analysis on IMDb movie reviews, served over a FastAPI HTTP API with
MLflow experiment tracking.

## Stack

| Layer      | Choice                                  |
| ---------- | --------------------------------------- |
| API        | FastAPI + Uvicorn                       |
| ML         | scikit-learn, pandas, NLTK, joblib      |
| Tracking   | MLflow (SQLite backend)                 |
| Packaging  | uv                                      |
| Runtime    | Docker + Docker Compose                 |

## Project layout

```
imdb-sentiment-analyzer/
├── data/
│   ├── raw/                  # source IMDb dataset (gitignored)
│   └── processed/            # cleaned/split data (gitignored)
├── notebooks/
│   └── 01_exploration.ipynb
├── app/
│   ├── main.py               # FastAPI app factory
│   ├── api/routes/
│   │   └── sentiment.py      # sentiment endpoints
│   ├── ml/
│   │   ├── preprocess.py     # text cleaning
│   │   ├── features.py       # vectorisation
│   │   ├── train.py          # model fitting + MLflow logging
│   │   ├── predict.py        # inference helpers
│   │   └── evaluate.py       # metrics
│   ├── schemas/
│   │   └── sentiment.py      # pydantic request/response models
│   └── core/
│       └── config.py         # settings
├── models/
│   └── sentiment_pipeline.pkl
├── tests/
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Setup

```bash
uv sync
```

Requires Python 3.14 (see `.python-version`).

## Run locally

```bash
uv run uvicorn app.main:app --reload
```

API docs at http://localhost:8000/docs

## Run with Docker

```bash
docker compose up --build
```

| Service | URL                     | Description                        |
| ------- | ----------------------- | ---------------------------------- |
| `api`   | http://localhost:8000  | FastAPI service                    |
| `mlflow`| http://localhost:5000  | MLflow tracking UI                 |

## Tests

```bash
uv run pytest
uv run ruff check .
```

## Notes

`models/*.pkl`, `mlflow.db`, and everything under `data/` are generated at
runtime and gitignored. Directories are kept in version control via `.gitkeep`.
