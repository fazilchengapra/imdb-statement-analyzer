import pandas as ps
from datasets import load_dataset
from app.ml.preprocess import clean_text

dataset = load_dataset("stanfordnlp/imdb")


train_df = dataset["train"].to_pandas()
test_df = dataset["test"].to_pandas()

train_df['clean_text'] = train_df['clean_text'] = train_df['text'].apply(clean_text)
test_df['clean_text'] = test_df['clean_text'] = train_df['text'].apply(clean_text)