"""
    Connect to S3
"""
import boto3
from src.constants import *
from src.exception import CustomException

class S3handler:
    s3_client=None
    s3_resource=None
    def __init__(self, bucket_name: str, region: str =AWS_REGION):
        self._access_key = AWS_ACCESS_KEY
        self._secret_key = AWS_SECRET_KEY
        if self._access_key is None:
            raise CustomException(f"Environment variable: ACCESS KEY is not set.")
        if self._secret_key is None:
            raise CustomException(f"Environment variable: ACCESS SECRET KEY is not set.")
        S3handler.s3_resource = boto3.resource('s3',
                                    aws_access_key_id=self._access_key_id,
                                    aws_secret_access_key=self._secret_access_key,
                                    region_name=AWS_REGION
                                    )
        S3handler.s3_client = boto3.client(
                            's3',
                            aws_access_key_id=self._access_key_id,
                            aws_secret_access_key=self._secret_access_key,
                            region_name=AWS_REGION
                            )
        
        self.s3_resource = S3handler.s3_resource
        self.s3_client = S3handler.s3_client