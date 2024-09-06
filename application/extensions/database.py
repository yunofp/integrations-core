from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import logging

logger = logging.getLogger(__name__)


def init_app(app):
    uri = app.config.get('MONGO_DATABASE_URI')
    database = app.config.get('MONGO_DATABASE_NAME')
    if not uri:
        raise ValueError("MongoDB database URI not found in configuration.")

    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        app.dbClient = client
        app.db = client.get_database(database)
        logger.info("init_app | Successfully connected to the MongoDB database.")

    except Exception as e:
        logger.error(f"Error connecting to the MongoDB database: {e}", exc_info=True)
        raise
