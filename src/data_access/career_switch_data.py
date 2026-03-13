from src.configuration.mongo_db_connection import MongoDbClient
from src.logger import get_logger
from src.exception import CustomException
import sys
import pandas as pd 
import inspect

logger = get_logger(__name__)

class CareerSwitchData:
    def __init__(self):
        try:
            self.client = MongoDbClient()
        except Exception as e: 
            raise CustomException( e, sys)
    

    def get_data_from_db(self):
        logger.info(f"{inspect.currentframe().f_code.co_name}")
        logger.info(f" Getting Data from mongodb")
        try:
            all_data = list(self.client.collection.find({}))
            df = pd.DataFrame(all_data)
            logger.info(f"Data Feched. Shape: {df.shape}")
            
            df.drop(['_id', 'enrollee_id'], axis=1, inplace=True)
            
            return df 
        except Exception as e: 
            raise CustomException(e, sys)            

