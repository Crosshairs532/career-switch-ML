from src.logger import get_logger
from src.cloud_storage.aws_storage import AWS_S3_Storage
import inspect

logger = get_logger(__name__)

class ModelPusher:
    def __init__(self, modelEvaluationArtifact):
        self.modelEvaluationArtifact = modelEvaluationArtifact
        self.aws_s3 = AWS_S3_Storage()

    def initiate_model_pusher(self):
        funct_name = inspect.currentframe().f_code.co_name
        logger.info(f"Entered {funct_name}")

        # create the folder or leave it if exists
        self.aws_s3.create_folder_s3('career_switch_model/')

        # upload model
        self.aws_s3.upload_to_s3( file=self.modelEvaluationArtifact.trained_model_path, key='career_switch_model/')

        
