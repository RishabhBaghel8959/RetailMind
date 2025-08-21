from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sentiment import clean_text, remove_stopwords, classify_sentiment, extract_topics, summarize_text
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔓 CORS so React (localhost:3000) can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewsIn(BaseModel):
    reviews: List[str]

@app.get("/")
def root():
    return {"status": "ok", "message": "API is running"}

@app.post("/analyze")
def analyze(body: ReviewsIn):
    out = []
    for review in body.reviews:
        cleaned = clean_text(review)
        normalized = remove_stopwords(cleaned)
        sentiment = classify_sentiment(normalized)
        topics = extract_topics(normalized)
        summary = summarize_text(normalized, max_tokens=40)
        out.append({
            "review": review,
            "cleaned_review": cleaned,
            "normalized_review": normalized,
            "sentiment": sentiment,
            "topics": topics,
            "summary": summary
        })
    return out
