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

        bucket_location = boto3.client("s3").get_bucket_location(Bucket=bucket)
        object_url = "https: //s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location["LocationConstraint"], bucket, filekey
        )

        return object_url

    def delete_file(self, file_id: str, filepath: str):
        filepath = filepath.split("/")[-1]
        bucket = "220103289-bucket"
        filekey = f"ads/{file_id}/{filepath}"

        self.s3.delete_object(Bucket=bucket, Key=filekey)
