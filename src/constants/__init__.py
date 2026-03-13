import os
from dotenv import load_dotenv
load_dotenv()
from datetime import date

PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"
FILE_NAME: str = "data.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

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
