from src.logger import get_logger
from src.pipline.training_pipeline import TrainPipeline
from src.components.model_evaluation import ModelEvaluation
from src.cloud_storage.aws_storage import AWS_S3_Storage

logger = get_logger(__name__)

train  = TrainPipeline()
train.run_pipeline()
# aws = AWS_S3_Storage()
# aws.get_all_resources()