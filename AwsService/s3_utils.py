from AwsService import s3_client, BUCKET_NAME
from botocore.exceptions import ClientError
import logging


def upload_file_to_s3(file_content, s3_key):
    """Uploads a file to the S3 bucket.

    Args:
        file_content (str or BytesIO): The file content to upload. If a string, it is the path to the file.
            If a BytesIO, it is the file content itself.
        s3_key (str): The key to use when storing the file in S3.

    Returns:
        bool: True if the file is uploaded successfully, False if there is an error.
    """
    if file_content is None:
        logging.error("File content cannot be None")
        return False
        
    try:
        s3_client.upload_file(file_content, Bucket=BUCKET_NAME, Key=s3_key)
    except ClientError as e:
        logging.error(f"AWS S3 upload error: {e}")
        return False
    except FileNotFoundError as e:
        logging.error(f"File not found: {file_content}")
        return False
    return True