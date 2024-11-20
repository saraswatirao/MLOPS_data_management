import boto3
from botocore.exceptions import NoCredentialsError
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME_1, S3_FILE_PATH, ORIGINAL_FILE_PATH

def upload_file_to_s3(access_key, secret_key, bucket_name, file_name, local_file_path):
    # Create an S3 client using the provided credentials
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        # Upload the local file to the specified S3 bucket with the given filename
        s3.upload_file(local_file_path, bucket_name, file_name)
        print(f"File '{file_name}' uploaded successfully to '{bucket_name}'")
    except FileNotFoundError:
        print(f"The file '{local_file_path}' does not exist")
    except NoCredentialsError:
        print("Credentials not available or incorrect")

if __name__ == "__main__":

    # Call the function to upload the file to S3
    upload_file_to_s3(AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME_1, S3_FILE_PATH, ORIGINAL_FILE_PATH)