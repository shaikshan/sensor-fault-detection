import logging
from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
def main():
    try:
        x = 1/0
        logging.info("dividing by zero")
    except Exception as e:
        raise SensorException(e,sys)
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    #moongodb_client = MongoDBClient()
    #print("collection_names:",moongodb_client.database.list_collection_names())