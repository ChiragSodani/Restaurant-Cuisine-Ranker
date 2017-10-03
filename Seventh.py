from pymongo import MongoClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

tags_collection = MongoClient('mongodb://localhost:27017/')['reviews_Tags']['reviews_Collection']
corpus_collection = MongoClient('mongodb://localhost:27017/')['reviews_Tags']['sentiment_Collection']

reviews_cursor = tags_collection.find()
reviewsCount = reviews_cursor.count()
reviews_cursor.batch_size(5000)

sid = SIA()
for review in reviews_cursor:
    ss = sid.polarity_scores(review["review"]) 
    maximum = max(list(ss.values())[0:3])
    for key,value in ss.items():
        if value == maximum:
            sentiment = key
    
    print("Processing Review No:",review["reviewNo"])
    corpus_collection.insert_one({
        "cityName": "Bangalore",
        "reviewNo": review["reviewNo"],
        "restaurantName": review["restaurantName"],
        "rating": review["rating"],
        "review": review["review"],
        "sentiment": sentiment,
        "score": maximum
    })