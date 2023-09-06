import certifi
from pymongo import MongoClient

from app.config import settings

client = MongoClient(settings.MONGODB_URL, tlsCAFile=certifi.where())

database_name = "fastapi_security"
db = client[database_name]


def connect_mongodb():
    try:
        client.admin.command("ping")
        print("Database Connection: ✅")
    except Exception as e:
        print("Database Connection: ❌", e)
