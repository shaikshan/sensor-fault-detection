import pymongo
from pymongo.mongo_client import MongoClient
from sensor.constants.database import DATABASE_NAME
import certifi
ca = certifi.where()
import os
from sensor.constants.env_variable import MONGODB_URL_KEY
class MongoDBClient:
    client = None
    def __init__(self,database_name=DATABASE_NAME):
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
                self.client = MongoDBClient.client
                self.database = self.client[database_name]
                self.database_name = database_name
        except Exception as e:
            raise e
