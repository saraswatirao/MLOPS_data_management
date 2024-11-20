import boto3
from botocore.exceptions import NoCredentialsError
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME_1, BUCKET_NAME_2, S3_FILE_PATH

def copy_file_between_buckets(access_key, secret_key, source_bucket, destination_bucket, file_name):
    # Create an S3 client using the provided credentials
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        # Copy the object (file) from the source bucket to the destination bucket
        copy_source = {'Bucket': source_bucket, 'Key': file_name}
        s3.copy_object(Bucket=destination_bucket, CopySource=copy_source, Key=file_name)
        
        print(f"File '{file_name}' copied successfully from '{source_bucket}' to '{destination_bucket}'")
    except NoCredentialsError:
        print("Credentials not available or incorrect")

if __name__ == "__main__":

    # Call the function to copy the file between S3 buckets
    copy_file_between_buckets(AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME_1, BUCKET_NAME_2, S3_FILE_PATH)
