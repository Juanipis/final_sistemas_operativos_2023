from typing import Dict, List
import boto3
import json
from logzero import logger
from pydantic_settings import BaseSettings


class S3Credentials(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket: str
    s3_region: str = 'us-west-1'
    drop_s3_bucket: bool = False



class S3Controller:
    def __init__(self, s3_credentials: S3Credentials):
        self.s3_bucket = s3_credentials.s3_bucket
        self.s3_client = boto3.client('s3', region_name=s3_credentials.s3_region,
                                        aws_access_key_id=s3_credentials.aws_access_key_id,
                                        aws_secret_access_key=s3_credentials.aws_secret_access_key)
        
        if s3_credentials.drop_s3_bucket:
            logger.info(f"Deleting bucket {s3_credentials.s3_bucket}")
            self.__empty_bucket(s3_credentials)

    def __empty_bucket(self, s3_credentials: S3Credentials):
        bucket_name = s3_credentials.s3_bucket
        objects = self.s3_client.list_objects_v2(Bucket=bucket_name)
        if "Contents" not in objects:
            return
        try:
            for object in objects["Contents"]:
                logger.info(f"Deleting {object['Key']}")
                self.s3_client.delete_object(Bucket=bucket_name, Key=object["Key"])

            for prefix in objects["CommonPrefixes"]:
                logger.info(f"Deleting {prefix['Prefix']}")
                self.s3_client.delete_object(Bucket=bucket_name, Key=prefix["Prefix"])
        except Exception as e:
            logger.error(f"Error deleting bucket {bucket_name}: {e}")
    
    def insert_json(self, json_data, s3_path):
        """
        Inserta un JSON en una ruta especificada en S3.

        :param json_data: Datos JSON a insertar.
        :param s3_path: Ruta en S3 donde se almacenará el archivo JSON.
        """
        json_str = json.dumps(json_data)
        
        self.s3_client.put_object(Body=json_str, Bucket=self.s3_bucket, Key=s3_path)
        return f"JSON guardado en {s3_path} en el bucket {self.s3_bucket}"
    

s3_controller = S3Controller(S3Credentials())
