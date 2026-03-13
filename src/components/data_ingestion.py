from src.logger import get_logger
from src.exception import CustomException
from src.entity.config_entity import DataIngestionConfig
from src.data_access.career_switch_data import CareerSwitchData
import sys
import inspect
from src.constants import *
from sklearn.model_selection import train_test_split
from src.entity.artifact_entity import DataIngestionArtifact


logger  = get_logger(__name__)
class DataIngestion:
    def __init__(self, dataIngestionconfig:DataIngestionConfig = DataIngestionConfig()):
        try: 
            self.data_ingestion_config = dataIngestionconfig
        except Exception as e: 
            logger.error("Something went wrong while data ingestion config initialization")
            raise CustomException(e,  sys)
        
    def save_data_to_feature_store(self):
        try: 
            CarrerSwitchdata =  CareerSwitchData()
            df = CarrerSwitchdata.get_data_from_db()
            logger.info(f"Got data in {inspect.currentframe().f_code.co_name}: {df.shape}")
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_path)
            os.makedirs(dir_path, exist_ok=True)
            logger.info("Saving data to feature Store..")
            df.to_csv(feature_store_path, index=False, header=True)
            logger.info("Data saved to Feature Store.")
            return df
        except Exception as e: 
            raise CustomException('Error while saving data to feature store' , sys)
    
    def train_test_split(self, df):
        logger.info("Train Test Split Entered")
        try:
            train_data, test_data = train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio)
            
            logger.info("Saving Train and Test data..")
            data_ingested = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(data_ingested, exist_ok=True)
            train_data.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_data.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logger.info("Train and Test data saved.")
        except Exception as e:
            raise CustomException(e, sys)
        
    def initialize_data_ingestion(self):
        funct_name = inspect.currentframe().f_code.co_name
       
        logger.info(f"Entered {funct_name}")

        try:
            df = self.save_data_to_feature_store()
            
            self.train_test_split(df)

            dataIngestionArtifact = DataIngestionArtifact(
                trained_file_path = self.data_ingestion_config.training_file_path,
                test_file_path = self.data_ingestion_config.testing_file_path
            )

            return dataIngestionArtifact

        except Exception as e: 
            raise CustomException("Error in {funct_name} ", sys)