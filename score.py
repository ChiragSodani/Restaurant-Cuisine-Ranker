from pymongo import MongoClient

random_collection = MongoClient('mongodb://localhost:27017/')['reviews_Tags']['sentiment_Collection']


dict_1 = {0: 'random', 1: 'noodle,bread',2: 'kebab,fruit', 3: 'random', 4: 'random', 5: 'cake,icecream,chocolate', 6: 'random', 7: 'samosa', 8: 'dosa,idli', 9: 'roll,roti', 10: 'Biryani,paneer', 11: 'puri,chat', 12: 'random', 13: 'sandwich', 14: 'aloo,pork', 15: 'random', 16: 'icecream,kulcha', 17: 'burger,chicken,beef', 18: 'kabab,tikka,tandoori', 19: 'beer,manchurian', 20: 'random', 21: 'dosa', 22: 'kababs', 23: 'brownie', 24: 'random', 25: 'egg', 26: 'chicken biryani', 27:'random', 28: 'random', 29: 'random', 30: 'sambhar,poha', 31: 'random', 32: 'random', 33: 'mutton', 34: 'random', 35: 'random', 36: 'meat', 37: 'vadapav,pavbhaji', 38:'random', 39: 'icetea', 40: 'chicken curry,mushroom salad', 41: 'random', 42: 'random', 43: 'pizza,chutney', 44: 'random', 45: 'coffee', 46: 'prawn,paratha', 47:'juice,paratha', 48: 'parathas', 49: 'random'}
score_list = {}

for i in dict_1:
	if dict_1[i] is not 'random':
		score = 0
		collection_count = random_collection.find().count()
    		for var in range(1,collection_count+1):
        		collection_entry = random_collection.find_one({"reviewNo":var})
        		if dict_1[i] in collection_entry['related_topics'] and collection_entry['sentiment'] is not "neg":
        			score = score + collection_entry['score']
			print("Processing Review No:",var,"for topic[",i,"]: ",dict_1[i])
		score_list[dict_1[i]] = score
        print score_list
print score_list
