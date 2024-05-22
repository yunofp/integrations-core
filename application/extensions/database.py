from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import logging

logger = logging.getLogger(__name__)

def init_app(app):
    uri = app.config.get('MONGO_DATABASE_URI')

    if not uri:
        raise ValueError("MongoDB database URI not found in configuration.")

    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        app.dbClient = client
        app.db = client.get_database("integration")
        print("Successfully connected to the MongoDB database.")
        logger.info("Successfully connected to the MongoDB database.")

    except Exception as e:
        print(f"Error connecting to the MongoDB database: {e}")
        logger.error(f"Error connecting to the MongoDB database: {e}", exc_info=True)
        raise
