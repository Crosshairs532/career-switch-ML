from src.configuration.aws_connection import S3handler
from src.constants import *
from src.logger import get_logger
from src.exception import CustomException
import sys
import dill
logger = get_logger(__name__)

class AWS_S3_Storage:
    def __init__(self):
        s3handler =  S3handler()
        self.s3_client = s3handler.s3_client
        self.s3_resource = s3handler.s3_resource
    
    def get_bucket(self, bucket_name=AWS_BUCKET_NAME):
        bucket = self.s3_resource.Bucket(bucket_name)
        
        return bucket
    def get_all_resources(self, path):
        bucket  = self.get_bucket()
        all_objects =  bucket.objects.filter(Prefix=path)
        files = []
        for obj in all_objects:
            if not obj.key.endswith('/'):
                files.append(obj.key)
      
        print(files)
        return files
    def upload_to_s3(self, file,  key ):
        
        try:
            bucket  = self.get_bucket()

            filename = os.path.basename(file)           
            s3_key   = key.rstrip('/') + '/' + filename 

            bucket.upload_file(file, s3_key)
            logger.info("Model file uploaded to s3")
        except Exception as e: 
            raise CustomException(e, sys) 


    
    def create_folder_s3(self, path):
        # check if folder exists. 

        folder_exist = self.get_all_resources(path)
        if folder_exist: 
            logger.info(" Folder already Exists: {career_switch_model/}")
        else: 
            self.s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key='career_switch_model/')
            logger.info(" Folder created: {career_switch_model/}")
    def load_model_s3(self, s3_key):
        try:
            bucket       = self.get_bucket()
            file_objects = list(bucket.objects.filter(Prefix=s3_key))

            
            file_objects = [obj for obj in file_objects if not obj.key.endswith('/')]

            if not file_objects:
                logger.info(f"No model found at: {s3_key}")
                return None

        
            model_bytes = file_objects[0].get()["Body"].read()
            model       = dill.loads(model_bytes)
            logger.info(f"Model loaded from S3: {file_objects[0].key}")
            return model

        except Exception as e:
            raise CustomException(e, sys)