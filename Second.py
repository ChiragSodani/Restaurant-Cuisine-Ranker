from pymongo import MongoClient
import nltk as np

reviews_collection = MongoClient('mongodb://localhost:27017/')['reviews_Database']['reviews_Collection']
tags_collection = MongoClient('mongodb://localhost:27017/')['reviews_Tags']['reviews_Collection']

reviews_cursor = reviews_collection.find()
reviewsCount = reviews_cursor.count()
#reviews_cursor.batch_size(1000)

stopwords = {}
with open('stopwords.txt', 'rU') as f:
    for line in f:
        stopwords[line.strip()] = 1

count = 0
for review in reviews_cursor:
    words = []
    sentences = np.sent_tokenize(review["review"].lower())

    for sentence in sentences:
        tokens = np.word_tokenize(sentence)
        text = [word for word in tokens if word not in stopwords]
        tagged_text = np.pos_tag(text)

        for word, tag in tagged_text:
            words.append({"word": word, "pos": tag})
    
    count = count + 1
    #print count
    print("Processing Review No.",review["reviewNo"],"Count is",count)
    tags_collection.insert_one({
        "cityName": "Bangalore",
        "reviewNo": count,
        "restaurantName": review["restaurantName"],
        "rating": review["rating"],
        "review": review["review"],
        "words": words
    })
