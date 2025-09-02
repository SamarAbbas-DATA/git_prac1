from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["blogdb"]
collection = db["blogs"]

collection2 = db['users']