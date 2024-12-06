from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")


db = client["KyoMDB_"]

word_collection = db["Words"]
interaction_collection = db["Interactions"]
