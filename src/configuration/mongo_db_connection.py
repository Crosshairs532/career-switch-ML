from src.logger import get_logger
from src.exception import CustomException
from src.constants import *
from pymongo import MongoClient
import sys

logger = get_logger(__name__)


class MongoDbClient: 
    client = None

    def __init__(self, db_name=None):
        logger.info("MongoDb Connecting...")
        try: 
            mongodb_uri = MONGODB_URI
            
            if mongodb_uri is None: 
                raise CustomException(f"Environment variable `MongoDBUri` is not set.", sys)
            if MongoDbClient.client is None: 
                MongoDbClient.client = MongoClient(mongodb_uri)

            self.database = MongoDbClient.client['CW']
            self.collection = self.database['career_switch']
            logger.info("MongoDb Connected.")
        except Exception as e: 
            raise CustomException(e, sys)