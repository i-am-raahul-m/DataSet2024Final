from transformers import pipeline


def analyze_query_sentiment(query):
    sentiment_analyzer = pipeline("sentiment-analysis")

    result = sentiment_analyzer(query)

    sentiment_label = result[0]['label']
    sentiment_score = result[0]['score']
    return sentiment_score, sentiment_label

if __name__ == "__main__":
    print(analyze_query_sentiment("I am not happy with the service"))