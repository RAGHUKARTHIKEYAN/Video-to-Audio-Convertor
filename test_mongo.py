from pymongo import MongoClient

# Replace with your actual MongoDB Atlas connection string
client = MongoClient("mongodb+srv://raghu_db_user:1234@cluster0.mkmqppl.mongodb.net/mydatabase?retryWrites=true&w=majority")

db = client["mydatabase"]       # your database name
collection = db["mycollection"] # your collection name

collection.insert_one({"name": "Raghu"})
print(collection.find_one({"name": "Raghu"}))
