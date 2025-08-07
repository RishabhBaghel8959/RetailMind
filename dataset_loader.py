from datasets import load_dataset

def load_reviews_from_huggingface(dataset_name="amazon_polarity", split="train", sample_size=1000):
    dataset = load_dataset(dataset_name, split=split)
    df = dataset.to_pandas()

    if 'content' in df.columns:
        df.rename(columns={'content': 'review'}, inplace=True)
    elif 'text' in df.columns:
        df.rename(columns={'text': 'review'}, inplace=True)

    df = df[['review']].dropna().sample(n=sample_size, random_state=42)
    return df

if __name__ == "__main__":
    df = load_reviews_from_huggingface()
    print(df.head())

    df.to_csv("reviews.csv", index=False)
    
