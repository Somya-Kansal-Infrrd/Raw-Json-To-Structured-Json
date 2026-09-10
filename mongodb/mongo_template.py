"""MongoDB connection and collection configuration."""

from pymongo import MongoClient


MONGO_URL = "mongodb://localhost:27017"
DATABASE_NAME = "json_to_json"

client = MongoClient(MONGO_URL)
client.admin.command("ping")

db = client[DATABASE_NAME]

mapping_collection = db["field_transformation_config"]
converted_collection = db["converted_documents"]