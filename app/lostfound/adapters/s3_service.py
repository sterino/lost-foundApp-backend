import os
from typing import BinaryIO

import boto3

aws_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_key = os.getenv("AWS_SECRET_ACCESS_KEY")


class S3Service:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def upload_file(self, file: BinaryIO, sh_id: str, filename: str):
        bucket = "aibatyr"
        filekey = f"ads/{sh_id}/{filename}"

        self.s3.upload_fileobj(file, bucket, filekey)

        object_url = "https://{0}.s3.amazonaws.com/ads/{1}/{2}".format(
            bucket, sh_id, filekey
        )

        return object_url

    def delete_file(self, file_id: str, filepath: str):
        filepath = filepath.split("/")[-1]
        bucket = "220103289"
        filekey = f"ads/{file_id}/{filepath}"

        self.s3.delete_object(Bucket=bucket, Key=filekey)
