from sensor.configuration.mongo_db_connection import MongoDBClient

if __name__ == "__main__":
    moongodb_client = MongoDBClient()
    print("collection_names:",moongodb_client.database.list_collection_names())