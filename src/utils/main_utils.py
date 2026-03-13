from src.logger import get_logger
from src.exception import CustomException
import yaml
import sys
logger = get_logger(__name__)

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            logger.info(f"Reading Yaml File: {file_path}")
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise CustomException(e, sys) from e