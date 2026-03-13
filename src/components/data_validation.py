from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import DataIngestionConfig
from src.exception import CustomException
import sys
import os
import pandas as pd

from src.exception import CustomException
from src.logger import get_logger
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.utils.main_utils import read_yaml_file
import json

logger = get_logger(__name__)

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig = DataValidationConfig()):

        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path="config/schema.yaml")
        except Exception as e:
            raise CustomException(e, sys)

    def validate_columns(self, dataframe: pd.DataFrame, dataset_name: str) -> bool:
        """
        Validates if all expected columns are present in the dataframe.
        Deliberately ignores data types.
        """
        try:
          
            expected_columns = list(self._schema_config["columns"].keys())
            
    
            if "target_column" in self._schema_config and "name" in self._schema_config["target_column"]:
                target_col = self._schema_config["target_column"]["name"]
                if target_col not in expected_columns:
                    expected_columns.append(target_col)


            actual_columns = dataframe.columns.tolist()
            
            validation_status = True
            

            for column in expected_columns:
                if column not in actual_columns:
                    logger.error(f"[{dataset_name}] Validation Failed: Missing expected column -> '{column}'")
                    validation_status = False
            
   
            for column in actual_columns:
                if column not in expected_columns:
                    logger.warning(f"[{dataset_name}] Validation Warning: Found unexpected extra column -> '{column}'. You might want to drop this in transformation.")

            return validation_status

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:

        try:
            logger.info("Starting Data Validation...")
            
            train_df = pd.read_csv(self.data_ingestion_artifact.trained_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)


            logger.info("Validating Training Data...")
            train_status = self.validate_columns(dataframe=train_df, dataset_name="Train Data")
            
            logger.info("Validating Testing Data...")
            test_status = self.validate_columns(dataframe=test_df, dataset_name="Test Data")


            overall_status = train_status and test_status
            


            report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir, exist_ok=True)

           
            validation_report = {
                "validation_status": overall_status,
                "message": "No Missing Column Found".strip() if(overall_status) else "Missing Column Found!!".strip()
            }

            with open(self.data_validation_config.validation_report_file_path, "w") as report_file:
                json.dump(validation_report, report_file, indent=4)
            

            if not overall_status:
                logger.error("Data Validation Failed. Check 'schema.yaml' against your MongoDB data.")
                raise Exception("Data Validation Failed: Missing required columns. Check logs for details.")

            logger.info("Data Validation Passed Successfully. All expected columns are present.")
            
   
            data_validation_artifact = DataValidationArtifact(
                validation_status=overall_status,
                validation_message="Validation Passed - Structure matches schema",
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )
            
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)