from src.components.data_ingestion import DataIngestionConfig
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.logger import get_logger

logger = get_logger(__name__)

class TrainPipeline: 
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
    
        logger.info("Training Pipeline Initialized.")
    
    def startDataIngestion(self):
        data_ingestion = DataIngestion()
        data_ingestion_artifact = data_ingestion.initialize_data_ingestion()
        return data_ingestion_artifact

    def startDataValidation(self, dataIngestionArtifact):
       data_validation = DataValidation(dataIngestionArtifact)
       data_validation_artifact = data_validation.initiate_data_validation()
       return data_validation_artifact

    def run_pipeline(self):
        logger.info("Data Ingestion Started.")
        dataIngestionArtifact = self.startDataIngestion()
        logger.info("Data Ingestion Finished.")

        logger.info("Data Validation Started.")
        dataValidationArtifact = self.startDataValidation(dataIngestionArtifact)
        logger.info("Data Validation Finished.")