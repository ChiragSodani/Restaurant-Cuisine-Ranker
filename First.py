from pymongo import MongoClient
import pandas as pd

df = pd.read_excel('bangalore.xlsx',index_col=False,encoding='utf8', names=['Review_No','Restaurant_Name','Rating','Review'])
#print df
reviews_collection = MongoClient('mongodb://localhost:27017/')['reviews_Database']['reviews_Collection']
for index, row in df.iterrows():
    reviews_collection.insert_one({
                "cityName": "Bangalore",
                "reviewNo": int(row['Review_No']),
                "restaurantName": row['Restaurant_Name'],
                "rating": row["Rating"],
                "review": row["Review"]
            })
