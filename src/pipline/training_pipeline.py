from src.components.data_ingestion import DataIngestionConfig
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher
from src.entity.config_entity import *
from src.logger import get_logger

logger = get_logger(__name__)

class TrainPipeline: 
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
    
        logger.info("Training Pipeline Initialized.")
    
    def startDataIngestion(self):
        data_ingestion = DataIngestion()
        data_ingestion_artifact = data_ingestion.initialize_data_ingestion()
        return data_ingestion_artifact

    def startDataValidation(self, dataIngestionArtifact):
       data_validation = DataValidation(dataIngestionArtifact)
       data_validation_artifact = data_validation.initiate_data_validation()
       return data_validation_artifact

    def startDataTranformation(self, dataIngestionArtifact, dataValidationArtifact):
        data_transformation = DataTransformation(dataIngestionArtifact, self.data_transformation_config, dataValidationArtifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        return data_transformation_artifact
    
    def startModelTraining(self, dataTransformationArtifact):
        model_trainer_artifact = ModelTrainer(dataTransformationArtifact, self.model_trainer_config)

        return model_trainer_artifact.initiate_model_training()
    
    def startModelEvaluation(self, dataIngestionArtifact, modelTrainerArtifact):
        model_evaluation = ModelEvaluation(dataIngestionArtifact, modelTrainerArtifact,self.model_evaluation_config )
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
        return model_evaluation_artifact
    
    def startModelPusher(self, modelEvaluationArtifact):
        model_pusher = ModelPusher(modelEvaluationArtifact)
        
        model_pusher_artifact = model_pusher.initiate_model_pusher()

        return model_pusher_artifact
    def run_pipeline(self):
        logger.info("Data Ingestion Started.")
        dataIngestionArtifact = self.startDataIngestion()
        logger.info("Data Ingestion Finished.")

        logger.info("Data Validation Started.")
        dataValidationArtifact = self.startDataValidation(dataIngestionArtifact)
        logger.info("Data Validation Finished.")

        logger.info("Data Transformation Started.")
        dataTransformationArtifact = self.startDataTranformation(dataIngestionArtifact, dataValidationArtifact)
        logger.info("Data Transformation Finished.")

        logger.info("Model Training Started.")
        modelTrainerArtifact = self.startModelTraining(dataTransformationArtifact)
        logger.info("Model Training Finished.")

        logger.info("Model Evaluation Started.")
        modelEvaluationArtifact = self.startModelEvaluation(dataIngestionArtifact, modelTrainerArtifact)
        logger.info("Model Evaluation Finished.")

        if not modelEvaluationArtifact.is_model_accepted:
            logger.info( "Keeping the old model")
            return

        logger.info("Model Pusher Started.")
        model_pusher_artifact = self.startModelPusher(modelEvaluationArtifact)

        