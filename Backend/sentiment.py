from datasets import load_dataset
import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from keybert import KeyBERT
from transformers import pipeline

# ----------------------------
# Setup
# ----------------------------
nltk.download('stopwords')
analyzer = SentimentIntensityAnalyzer()
kw_model = KeyBERT(model="all-MiniLM-L6-v2")

print("⏳ Loading T5 summarization model...")
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

# ----------------------------
# Step 1: Load dataset
# ----------------------------
def load_reviews_from_huggingface(dataset_name="amazon_polarity", split="train", sample_size=500):
    dataset = load_dataset(dataset_name, split=split)
    df = dataset.to_pandas()

    if 'content' in df.columns:
        df.rename(columns={'content': 'review'}, inplace=True)
    elif 'text' in df.columns:
        df.rename(columns={'text': 'review'}, inplace=True)

    df = df[['review']].dropna().sample(n=sample_size, random_state=42)
    return df

# ----------------------------
# Step 2: Clean text
# ----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ----------------------------
# Step 3: Remove stopwords
# ----------------------------
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = text.split()
    filtered = [w for w in word_tokens if w not in stop_words]
    return ' '.join(filtered)

# ----------------------------
# Step 4: Sentiment analysis
# ----------------------------
def classify_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return 'positive'
    elif compound <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# ----------------------------
# Step 5: Topic extraction
# ----------------------------
def extract_topics(text):
    if not text.strip():
        return ""
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=3
    )
    return ", ".join([kw for kw, score in keywords])

# ----------------------------
# Step 6: Summarization (safe, no warnings or '<' error)
# ----------------------------
def summarize_text(text, max_tokens=40):
    if not text.strip() or len(text.split()) < 5:
        return text  # Skip summarizing empty/short reviews
    try:
        summary = summarizer(
            text,
            max_new_tokens=max_tokens,
            min_length=10,
            max_length=len(text.split()) + max_tokens,  # Dynamic safe limit
            do_sample=False
        )
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error: {str(e)}"

# ----------------------------
# Step 7: Full preprocessing pipeline
# ----------------------------
def preprocess_reviews(df):
    df['cleaned_review'] = df['review'].apply(clean_text)
    df['normalized_review'] = df['cleaned_review'].apply(remove_stopwords)
    df['sentiment'] = df['normalized_review'].apply(classify_sentiment)
    df['topics'] = df['normalized_review'].apply(extract_topics)
    df['summary'] = df['normalized_review'].apply(lambda x: summarize_text(x, max_tokens=40))
    return df

# ----------------------------
# Step 8: Save results
# ----------------------------
def save_results(df, output_path='huggingface_reviews_full_pipeline.csv'):
    df[['review', 'normalized_review', 'sentiment', 'topics', 'summary']].to_csv(output_path, index=False)
    print(f"\n✅ Data with sentiment, topics & summary saved to: {output_path}")

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    print("📥 Loading dataset...")
    df = load_reviews_from_huggingface("amazon_polarity", "train", 500)

    print("🧹 Processing reviews...")
    df = preprocess_reviews(df)

    print("\n📊 First 10 processed rows:\n")
    print(df.head(10))

    save_results(df)
