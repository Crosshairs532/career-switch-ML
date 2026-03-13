from src.logger import get_logger
from src.data_access.career_switch_data import CareerSwitchData
from src.pipline.training_pipeline import TrainPipeline
logger = get_logger(__name__)

train  = TrainPipeline()

train.run_pipeline()
