from src.logger import get_logger
from src.exception import CustomException
from src.utils.main_utils import load_object
from src.entity.artifact_entity import *
from src.entity.config_entity import *
from sklearn.metrics import f1_score
from src.cloud_storage.aws_storage import AWS_S3_Storage
import  pandas as pd
import numpy as np
import inspect
import sys


logger = get_logger(__name__)


class ModelEvaluation:
    def __init__(self, dataIngestionArtifact, modelTrainerArtifact, modelEvaluationconfig):
        self.model_eval_config = modelEvaluationconfig
        self.data_ingestion_artifact = dataIngestionArtifact
        self.model_trainer_artifact = modelTrainerArtifact
        self.aws_s3_storage = AWS_S3_Storage()

    def correct_city_column(self, df):
        df["city"] = df["city"].str.split("_", expand=True)[1]
        df["city"] = df["city"].astype("int")
        return df

    def map_relevant_experience(self, df):
        df["relevent_experience"] = np.where(df["relevent_experience"] == 'Has relevent experience', 1, 0)
        return df

    def map_experience(self, df):
        
        df["experience"] = df["experience"].replace({"<1": "0", ">20": "21"})
        df["experience"] = df["experience"].astype(float) 

        return df
    
    def map_company_size(self, df):
        size_mapping = {
            "10000+": "10000-20000", 
            "Oct-49": "10-49", 
            "<10": "1-9"
        }
        df["company_size"] = df["company_size"].replace(size_mapping)
        df[["company_size_min", "company_size_max"]] = df["company_size"].str.split("-", expand=True)
        df["company_size_min"] = pd.to_numeric(df["company_size_min"], errors='coerce')
        df["company_size_max"] = pd.to_numeric(df["company_size_max"], errors='coerce')
        df[["company_size_min", "company_size_max"]] = df[["company_size_min", "company_size_max"]].fillna(0).astype(int)
        df.drop("company_size", axis=1, inplace=True)
        return df
    
    def map_last_new_job(self, df):
        df['last_new_job'] = df['last_new_job'].replace({'>4': '5', 'never': '0'})
        df['last_new_job'] = df['last_new_job'].astype(float)
        return df
     
    def remove_outlier(self, df):
        percentile25 = df['training_hours'].quantile(0.25)
        percentile75 = df['training_hours'].quantile(0.75)
        iqr = percentile75 - percentile25
        upper_limit = percentile75 + 1.5 * iqr
        lower_limit = percentile25 - 1.5 * iqr

        df[(df["training_hours"] > upper_limit) | (df["training_hours"]< lower_limit)]

        # capping
        df["training_hours"] = np.where(df["training_hours"] > upper_limit, upper_limit, np.where(df["training_hours"]<lower_limit, lower_limit,df["training_hours"]))

        return df
   

    def get_aws_s3_model(self):
        s3_model = self.aws_s3_storage.load_model_s3('career_switch_model/')
        return s3_model
    def model_evaluation(self):
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logger.info(f"Test data Loaded: {test_df.shape}")
            logger.info("Test data Preprocessing.")
            test_df = self.correct_city_column(test_df)
            test_df = self.map_relevant_experience(test_df)
            test_df = self.map_experience(test_df)
            test_df = self.map_company_size(test_df)
            test_df = self.map_last_new_job(test_df)
            test_df = self.remove_outlier(test_df)

            # x, y = test_df.drop('will_change_career', axis=1), test_df['will_change_career']



            logger.info("Test data preprocessing Done.")
            logger.info("Loading the Trained Model.")
            train_model = load_object(self.model_trainer_artifact.trained_model_file_path)
            logger.info("Loaded the Trained Model.")
            logger.info("Load the Best Model From AWS S3.")
    


            train_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
            best_model = self.get_aws_s3_model()
            best_model_f1_score = None
            if best_model is not None: 
                y_hat_best_model = best_model.predict(test_df.drop("will_change_career", axis=1))
                best_model_f1_score = f1_score(test_df["will_change_career"], y_hat_best_model)

            temp_score = best_model_f1_score if best_model_f1_score is not None else 0  

            model_response =  EvaluateModelResponse(
                trained_model_f1_score = train_model_f1_score, 
                best_model_f1_score = best_model_f1_score, 
                is_model_accepted=  train_model_f1_score  >  temp_score,
                difference = train_model_f1_score - temp_score
            )

            return model_response

        except Exception as e:
            raise CustomException(e, sys)
    def initiate_model_evaluation(self):
        funct_name = inspect.currentframe().f_code.co_name
        logger.info(f"Entered {funct_name}")

        model_evaluation = self.model_evaluation()

        model_evaluation_artifact = ModelEvaluationArtifact(
            is_model_accepted= model_evaluation.is_model_accepted,
            s3_model_path= self.model_eval_config.s3_model_key_path,
            trained_model_path=self.model_trainer_artifact.trained_model_file_path,
            changed_accuracy=model_evaluation.difference
        )
        return model_evaluation_artifact

