from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

analyzer = SentimentIntensityAnalyzer()

def preprocess_text(text):
    # Simplify text preprocessing to speed up analysis
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.lower()  # Convert to lowercase
    return text.strip()

def analyze_sentiment(text):
    # Preprocess text before analysis
    text = preprocess_text(text)
    sentiment_score = analyzer.polarity_scores(text)['compound']
    if sentiment_score > 0.05:
        return "Positive"
    elif sentiment_score < -0.05:
        return "Negative"
    else:
        return "Neutral"
