from pymongo import MongoClient
from nltk.stem.wordnet import WordNetLemmatizer

tags_collection = MongoClient('mongodb://localhost:27017/')['reviews_Tags']['reviews_Collection']
corpus_collection = MongoClient('mongodb://localhost:27017/')['reviews_Tags']['noun_corpus_Collection']

reviews_cursor = tags_collection.find()
reviewsCount = reviews_cursor.count()
reviews_cursor.batch_size(5000)

lem = WordNetLemmatizer()

for review in reviews_cursor:
    nouns = []
    words = [word for word in review["words"] if word["pos"] in ["NN", "NNS"]]

    for word in words:
        nouns.append(lem.lemmatize(word["word"]))

    corpus_collection.insert_one({
        "cityName": "Bangalore",
        "reviewNo": review["reviewNo"],
        "restaurantName": review["restaurantName"],
        "rating": review["rating"],
        "review": review["review"],
        "words": nouns
    })
