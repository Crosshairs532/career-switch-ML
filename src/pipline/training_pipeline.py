from src.components.data_ingestion import DataIngestionConfig
from src.components.data_ingestion import DataIngestion
from src.logger import get_logger

logger = get_logger(__name__)

class TrainPipeline: 
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
    
    def startDataIngestion(self):
        data_ingestion = DataIngestion()
        data_ingestion_artifact = data_ingestion.initialize_data_ingestion()
        return data_ingestion_artifact

    def run_pipeline(self):
        logger.info("Data Ingestion Started.")
        dataIngestionArtifact = self.startDataIngestion()
        logger.info("Data Ingestion Finished.")