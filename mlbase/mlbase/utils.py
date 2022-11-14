import os
import pickle

import numpy as np
import boto3

from botocore.client import Config


class ClientS3:
    SERVICE_NAME = 's3'
    SIGNATURE_VERSION = 's3v4'
    REGION_NAME = 'us-east-1'

    def __init__(
        self,
        endpoint_url: str,
        aws_access_key_id: str,
        aws_secret_access_key: str
    ):
        self._client = boto3.resource(
            self.SERVICE_NAME,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version=self.SIGNATURE_VERSION),
            region_name=self.REGION_NAME
        )

    def load_from_s3(self, bucket: str, remote_path: str, local_path: str):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        self._client.Bucket(bucket).download_file(remote_path, local_path)

    def upload_to_s3(
        self,
        bucket: str,
        remote_path: str,
        local_path: str,
    ):
        self._client.Bucket(bucket).upload_file(local_path, remote_path)

    def get_object(self, bucket: str, path: str):
        object = self._client.Object(bucket, path)
        return object.get()['Body'].read().decode()


def write_array(array: np.ndarray, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as file:
        pickle.dump(obj=array, file=file)


def read_array(path: str):
    with open(path, 'rb') as file:
        return pickle.load(file=file)


def write_task_result(value, path):
    with open(path, "wt") as file:
        file.write(value)


