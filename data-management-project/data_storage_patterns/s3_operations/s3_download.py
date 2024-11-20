import boto3
from botocore.exceptions import NoCredentialsError
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME_1, DOWNLOADED_FILE_PATH, S3_FILE_PATH

def download_file_from_s3(access_key, secret_key, bucket_name, file_name, local_file_path):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        s3.download_file(bucket_name, file_name, local_file_path)
        print(f"File '{file_name}' downloaded successfully to '{local_file_path}'")
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist in the bucket '{bucket_name}'")
    except NoCredentialsError:
        print("Credentials not available or incorrect")

if __name__ == "__main__":

    download_file_from_s3(AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME_1, S3_FILE_PATH, DOWNLOADED_FILE_PATH)