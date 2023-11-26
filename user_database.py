import pymongo
from pymongo import MongoClient
import os

user = os.environ.get("DB_USER")
secret = os.environ.get("DB_PASS")

cluster = pymongo.MongoClient("mongodb+srv://manish05:manish05@cluster0.z3buhby.mongodb.net/?retryWrites=true&w=majority")

db = cluster["pymongo_auth"]
collection = db["users"]


def add_user(user):
    return collection.insert_one(user)


def check_for_user(email, da):
    if collection.find_one({"email": email}) and collection.find_one({"da": da}):
        return True
    else:
        return False


def get_user(email):
    return collection.find_one({"email": email})




