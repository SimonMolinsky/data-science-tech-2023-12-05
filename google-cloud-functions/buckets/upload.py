import gzip
import json
import logging
from typing import Dict

from google.cloud import storage
from google.cloud.storage import fileio


def upload_to_cloud_storage(json_string: str, bucket_name: str, filename: str, gzip_data=True):
    """Gzip and write to Cloud Storage.

    Fn source: https://stackoverflow.com/questions/73663848/gzip-a-file-in-python-before-uploading-to-cloud-storage

    :param json_string: JSON with a data
    :param bucket_name:
    :param filename:
    :param gzip_data: bool

    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Filename (include path)
    blob = bucket.blob(filename)

    if gzip_data:
        # Set blog meta data for decompressive transcoding
        blob.content_encoding = 'gzip'
        blob.content_type = 'application/json'

        writer = fileio.BlobWriter(blob)

        # Must write as bytes
        gz = gzip.GzipFile(fileobj=writer, mode="wb")

        # When writing as bytes we must encode our JSON string.
        gz.write(json_string.encode('utf-8'))

        # Close connections
        gz.close()
        writer.close()
    else:
        blob.content_type = 'text/plain'
        blob.upload_from_string(json_string)


def bucket_upload(ds: Dict,
                  filename: str,
                  bucket_name,
                  gzip_data=False):
    """
    Function prepares and uploads data into bucket.
    :param ds: Dict (data)
    :param filename: str
    :param bucket_name: str
    :param gzip_data: bool
    :return:
    """

    # Upload current
    upload_to_cloud_storage(
        json.dumps(ds), bucket_name=bucket_name, filename=filename, gzip_data=gzip_data
    )
    logging.info('INFO:APP:Data pushed into a bucket')
