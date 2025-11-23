import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from app.infra.mongodb.mongo_unit_of_work import MongoUnitOfWork

load_dotenv() 

def get_mongo_unit_of_work() -> MongoUnitOfWork:
    mongo_uri = os.getenv("MONGODB_URI")
    client = AsyncIOMotorClient(mongo_uri)
    return MongoUnitOfWork(client)


