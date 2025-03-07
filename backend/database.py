# from pymongo import MongoClient

# MONGO_URI = " "
# DB_NAME = "file_storage"

# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# users_collection = db["users"]
# files_collection = db["files"]

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

DB_NAME = "file_storage"
uri = "mongodb+srv://admin:cractus69@cluster0.kgxfebe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[DB_NAME]
users_collection = db["users"]
files_collection  = db["files"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)