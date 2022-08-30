import os

from storages.backends.s3boto3 import S3Boto3Storage


class AWSMediaStorage(S3Boto3Storage):
    bucket_name = os.getenv('AWS_BUCKET', 'transit-dev-files')
