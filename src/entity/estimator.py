from src.logger import get_logger
from src.exception import CustomException
import pandas as pd
import numpy as np
import sys
import os

logger = get_logger(__name__)

class MyModel:
    def __init__(self, preprocessing_object, trained_model_object):

        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object


    def custom_preprocessing(self, df):
 
        df = df.copy() 
    
        if "city" in df.columns:
            df["city"] = df["city"].astype(str).apply(
                lambda x: int(x.split("_")[1]) if "_" in x else int(x)
            )
                    
        if "relevent_experience" in df.columns:
            df["relevent_experience"] = np.where(df["relevent_experience"] == 'Has relevent experience', 1, 0)

        if "experience" in df.columns:
            df["experience"] = df["experience"].replace({"<1": "0", ">20": "21"}).astype(float)
            
        if "company_size" in df.columns:
            size_mapping = {"10000+": "10000-20000", "Oct-49": "10-49", "<10": "1-9"}
            df["company_size"] = df["company_size"].replace(size_mapping)
          
            df[["company_size_min", "company_size_max"]] = df["company_size"].str.split("-", n=1, expand=True)
            df["company_size_min"] = pd.to_numeric(df["company_size_min"], errors='coerce')
            df["company_size_max"] = pd.to_numeric(df["company_size_max"], errors='coerce')
            df.drop("company_size", axis=1, inplace=True)
            
        if "last_new_job" in df.columns:
            df['last_new_job'] = df['last_new_job'].replace({'>4': '5', 'never': '0'}).astype(float)
            
        return df
    def predict(self, dataframe):

        try:
            logger.info("Starting prediction process.")
            print(dataframe.columns)
            dataframe = self.custom_preprocessing(dataframe)
            logger.info("Custom Preprocessing DONE.")
            transformed_feature = self.preprocessing_object.transform(dataframe)
            logger.info("Using the trained model to get predictions")
            predictions = self.trained_model_object.predict(transformed_feature)

            return predictions

        except Exception as e:
            logger.error("Error occurred in predict method", exc_info=True)
            raise CustomException(e, sys) from e


    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"