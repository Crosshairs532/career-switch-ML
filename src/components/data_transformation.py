from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from src.logger import get_logger
from src.exception import CustomException
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, PowerTransformer, MinMaxScaler
from src.utils.main_utils import *
import numpy as np
import pandas as pd
import sys
import os
import inspect

logger = get_logger(__name__)

class DataTransformation:
    def __init__(self, dataIngestionArtifact:DataIngestionArtifact, 
                 dataTransformationconfig:DataTransformationConfig, 
                 dataValidationArtiact:DataValidationArtifact):
        try:
            self.data_ingestion_artifact =  dataIngestionArtifact
            self.data_validation_artifact = dataValidationArtiact
            self.data_transformation_config = dataTransformationconfig
        except Exception as e:
            raise CustomException(e, sys)
    def correct_city_column(self, df):
        df["city"] = df["city"].str.split("_", expand=True)[1]
        df["city"] = df["city"].astype("int")
        return df

    def map_relevant_experience(self, df):
        df["relevent_experience"] = np.where(df["relevent_experience"] == 'Has relevent experience', 1, 0)
        return df
    
    # def impute_enrolled_university(self, df):
    #     impute_mode  = SimpleImputer(strategy='most_frequent')
    #     df["enrolled_university"] = impute_mode.fit_transform(df[["enrolled_university"]]).ravel()
    #     return df

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
        df.drop("company_size", axis=1, inplace=True)
        return df
    def map_last_new_job(self, df):
        df['last_new_job'] = df['last_new_job'].replace({'>4': '5', 'never': '0'})
        df['last_new_job'] = df['last_new_job'].astype(float)
        return df
    

    def get_data_transformer_object(self) -> ColumnTransformer:

        logger.info("get_data_transformer_object")
        try:  

            cat_high_nulls = ["gender", "company_type", "major_discipline"]
            

            low_missing_cols_nominal = ["enrolled_university"]
            low_missing_col_ordinal = ["education_level"]      

            num_cols = ['city_development_index', 'experience', 'last_new_job', 'training_hours', 'company_size_max']
            
            

            high_missing_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
                ("onehot", OneHotEncoder(sparse_output=False, drop="first", handle_unknown='ignore'))
            ])

   
            low_miss_nominal_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(sparse_output=False, drop="first", handle_unknown='ignore'))
            ])


            edu_categories = ["Primary School", "High School", "Graduate", "Masters", "Phd", "Unknown"]
            ord_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("ordinal", OrdinalEncoder(categories=[edu_categories], 
                                           handle_unknown='use_encoded_value', unknown_value=-1))
            ])


            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("power", PowerTransformer(method='yeo-johnson'))
            ])



            preprocessor = ColumnTransformer(
                transformers=[
                    ("cat_high", high_missing_pipeline, cat_high_nulls),
                    ("low_miss_nom", low_miss_nominal_pipeline, low_missing_cols_nominal),
                    ("ord_edu", ord_pipeline, low_missing_col_ordinal),
                    ("num", num_pipeline, num_cols)
                    
                ],
                remainder='passthrough'
            )

            
            final_pipeline = Pipeline(steps=[
                ("preprocessor", preprocessor),
                ("scaler", MinMaxScaler())
            ])

            logger.info("pipeline creation done")
            return final_pipeline
        except Exception as e: 
            raise CustomException(e, sys)
   
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
    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self):
        funct_name = inspect.currentframe().f_code.co_name
        logger.info(f"Entered {funct_name}")
        try:
            logger.info("!!! Data Transformation Started !!!")
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)

            train_df = self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            

            logger.info(type(train_df))
            logger.info("Train and Test dataset loaded")


            logger.info("Handling Train df.")
            train_df = self.correct_city_column(train_df)
            train_df = self.map_relevant_experience(train_df)
            # train_df = self.impute_enrolled_university(train_df)
            train_df = self.map_experience(train_df)
            train_df = self.map_company_size(train_df)
            train_df = self.map_last_new_job(train_df)
            train_df = self.remove_outlier(train_df)
            logger.info("Handled Train df.")


            logger.info("Handling Test df.")
            test_df = self.correct_city_column(test_df)
            test_df = self.map_relevant_experience(test_df)
            # test_df = self.impute_enrolled_university(test_df)
            test_df = self.map_experience(test_df)
            test_df = self.map_company_size(test_df)
            test_df = self.map_last_new_job(test_df)
            test_df = self.remove_outlier(test_df)
            logger.info("Handled test df.")

            logger.info("Getting Preprocessor object.")
            preprocessor = self.get_data_transformer_object()
            logger.info("Got Preprocessor object.")


            logger.info("Fit and Transform on Training df.")
            preprocessed_train_arr = preprocessor.fit_transform(train_df)

            logger.info("Transform on Testing df.")
            preprocessed_test_arr = preprocessor.transform(test_df)

            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=preprocessed_train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=preprocessed_test_arr)
            logger.info("Saved transformation objects")

            logger.info("Data transformation completed successfully")
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )


        except Exception as e: 
            raise CustomException(e, sys)



