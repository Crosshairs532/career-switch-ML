import os
from dotenv import load_dotenv
load_dotenv()
from datetime import date

PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"
FILE_NAME: str = "data.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"


# Database
MONGODB_URI=os.getenv("MONGODB_URI")

# Config
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

# Data Ingestion 
DATA_INGESTION_COLLECTION_NAME: str = "career_switch"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25

# Data Validation
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME: str = "report.yaml"

# Data Transformation
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"


# Model Training
MODEL_FILE_NAME = "model.pkl"
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")
MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 5
MIN_SAMPLES_SPLIT_CRITERION: str = 'entropy'

# AWS 
AWS_REGION= "ap-souteast-1"
AWS_ACCESS_KEY= os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY= os.getenv('AWS_SECRET_ACCESS_KEY')