from datasets import load_dataset
import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords


nltk.download('stopwords')


def load_reviews_from_huggingface(dataset_name="amazon_polarity", split="train", sample_size=1000):
    dataset = load_dataset(dataset_name, split=split)
    df = dataset.to_pandas()

    if 'content' in df.columns:
        df.rename(columns={'content': 'review'}, inplace=True)
    elif 'text' in df.columns:
        df.rename(columns={'text': 'review'}, inplace=True)

    df = df[['review']].dropna().sample(n=sample_size, random_state=42)
    return df


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = text.split()  
    filtered = [w for w in word_tokens if w not in stop_words]
    return ' '.join(filtered)


def preprocess_reviews(df):
    df['cleaned_review'] = df['review'].apply(clean_text)
    df['normalized_review'] = df['cleaned_review'].apply(remove_stopwords)
    return df


def save_cleaned_data(df, output_path='huggingface_cleaned_reviews.csv'):
    df[['review', 'normalized_review']].to_csv(output_path, index=False)
    print(f" Cleaned data saved to: {output_path}")

if __name__ == "__main__":
    df = load_reviews_from_huggingface("amazon_polarity", "train", 1000)
    df = preprocess_reviews(df)

   
    print(df.head(10))

    save_cleaned_data(df)

