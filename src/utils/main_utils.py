from src.logger import get_logger
from src.exception import CustomException
import numpy as np
import yaml
import sys
import inspect
import os
import dill


logger = get_logger(__name__)

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            logger.info(f"Reading Yaml File: {file_path}")
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise CustomException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    funct_name = inspect.currentframe().f_code.co_name
    logger.info(f"Entered {funct_name}")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logger.info(f"Exited {funct_name}")

    except Exception as e:
        raise CustomException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CustomException(e, sys) 